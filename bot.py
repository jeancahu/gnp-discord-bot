# GNP Bot

from discord import Embed, Member, Intents, utils # Bot TODO
from discord import __version__ as discord_version
from discord.ext import commands # it's no needed for 1.7.3> # TODO (Change on 1.7.3 release)

import paho.mqtt.client as mqtt
import asyncio

from sys import exit
from time import sleep, time
from random import choice, sample
from AntiScam import AntiScam

from asyncio import gather

from commands import ping, name
from constants import user_list, gnp_guild_id, bots_id

import re

from inspect import getmembers # TODO Remove
from mudae import MudaeTuRecord, MudaeClaimEmbed

import signal
from utils import \
    print_colors, \
    print_member_list, \
    if_zoo_print, \
    compute_for_owo, \
    compute_for_nonbots, \
    compute_for_dankmemer

def handler_stop_signals(signal, frame):
    print("Good bye!")
    exit(0)

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

## Decorators
def guild_only(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

def only_for_user(user_id): # Functions who returns a decorator
    async def predicate(ctx):
        if not ctx.author.id == user_id:
            authored_user = utils.get(ctx.guild.members, id=user_id)
            new_message = await ctx.send("Hey, you are not {}!".format(authored_user.display_name))
            sleep(3)
            await new_message.delete()
            await ctx.message.delete()
            return False
        return True
    return commands.check(predicate)

try:
    TOKEN = open("TOKEN").readline().replace('\n','')
except Exception as e:
    print(e)
    exit(1)

if not TOKEN:
    exit(2)

## Global variables

COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_BLUE="\033[0;34m"
COLOR_PURPLE="\033[0;35m"
COLOR_YELLOW="\033[1;33m"
COLOR_END="\033[0m"

## MQTT Client initialization
broker_address = "localhost"
broker_topic = "discord"

mqtt_client = mqtt.Client("P1")
mqtt_enable = True
try:
    mqtt_client.connect(broker_address)
except ConnectionRefusedError:
    print("MQTT server not found")
    mqtt_enable = False

## Mudae $tu buffer:
mudae_tu_buffer = list()

## Discord bot initialization
intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)
bot.remove_command("help")

log_channel = None

class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]] # Remove everyone role!

@bot.check
async def globally_block_dms(ctx):
    # Block DMs
    return ctx.guild is not None

@bot.listen()
async def on_ready():
    print("Bot is online, Pycord version: {}".format(discord_version))
    guild = utils.get(bot.guilds, id=gnp_guild_id)
    print(guild.name)

    print_member_list(guild)
    print_colors(guild)

@bot.listen()
async def on_member_join(member):
    member_role = utils.get(member.guild.roles, name="member")
    bots_role = [ role for role in member.guild.roles if role.name.lower() == 'bots' ]

    if member.guild.id == gnp_guild_id: ## Config for gaenabs
        await member.edit(nick=member.display_name.upper())

    if bots_role and member.bot:
        await member.add_roles(bots_role[0])
        return

    ## Add the member role to a new guild member
    if member_role and not member.bot:
        ## TODO Verify if the account is real
        await member.add_roles(member_role)
        return

@bot.listen()
async def on_member_update(before, after):
    # If is needed to avoid recursivity
    if after.guild.id == gnp_guild_id: # Only for gnp
        if not after.display_name == after.display_name.upper():
            await after.edit(nick=after.display_name.upper())

@bot.listen()
async def on_message(message):
    global mqtt_enable
    ## Bot itself
    if message.author.id == bots_id["homuri"]: # Bot itself
        return

    ## Non bot
    if not message.author.bot:
        await compute_for_nonbots(message) # for nonbots
        return

    ## only for bots
    if message.author.id == bots_id["owo"]: # OwO bot
        await compute_for_owo(message)
        return

    ## dankmemer
    if message.author.id == bots_id["dankmemer"]: # Dank Memer bot
        await compute_for_dankmemer(message)
        return


    try:
        # Init a mudae $tu record object
        if message.author.id == bots_id["mudae"]: # Mudae Bot
            mudae_tu_record_temp = MudaeTuRecord(message)
            mudae_tu_record_temp.save()
            return
    except ValueError as e:
        pass
    except TypeError as e:
        pass

    if message.author.id == bots_id["mudae"]: # Mudae Bot
        ## Special processing for $tu output
        try:
            embeds = getattr(message, "embeds")
            if len(embeds) == 1: # An embed only:
                if mqtt_enable:
                    mqtt_message = "Embed on message -> Title (author): {}\nTitle: {}\nDescription: {}".format(
                        embeds[0].author.name,
                        embeds[0].title,
                        embeds[0].description.split('\n')[0])
                    mqtt_client.publish(broker_topic, mqtt_message) # Publish
            else:
                pass

        except Exception as e: # There is not Embed
            pass
        return

@bot.listen()
async def on_reaction_add(reaction, user):
    if user.id == bots_id["homuri"]: # Bot itself
        return

    try:
        # Init a mudaeClimEmbed record object
        mudae_claim_embed_temp = MudaeClaimEmbed(reaction=reaction, user=user)
        # return
    except AttributeError as e:
        pass
    except ValueError as e:
        pass
    except TypeError as e:
        pass


@bot.command()
@commands.has_permissions(administrator=True)
async def count_msgs(ctx):

    # owo_bot = utils.get(ctx.guild.members, id=bots_id["owo"])
    messages = await ctx.channel.history(limit=10000).flatten()
    messages_owo = [ i for i in messages if "The coin spins" in i.content ]
    messages_owo_won = [ i for i in messages_owo if "you won" in i.content ]

    print("Messages amount: {}, Won: {}".format(len(messages_owo), len(messages_owo_won)))

@bot.command()
@commands.has_permissions(administrator=True)
async def meml(ctx):
    """
    Member list
    """
    guild = ctx.guild # Do it for every guild
    member_list = "\n".join([member.display_name for member in guild.members if not member.bot])
    await ctx.send(member_list)

@bot.command()
@commands.has_permissions(administrator=True)
@guild_only(gnp_guild_id) # Works for gnp server only
async def upper(ctx):
    """
    Uppercase name for each member
    """
    guild = utils.get(bot.guilds, id=gnp_guild_id)
    task_list = []
    for member in [ member for member in guild.members if member.top_role.name == "member"]:
        ## Edit nickname to upper case
        if member.display_name.upper() != member.display_name:
            try:
                task_list.append(
                    asyncio.create_task(member.edit(nick=member.display_name.upper()))
                )
            except Exception as e:
                pass

    for task in task_list:
        await task
    await ctx.message.add_reaction("👍")

# @bot.command() # Disabled due on_member_update listener
@commands.has_permissions(administrator=True)
@guild_only(gnp_guild_id) # Works for gnp server only
async def lower(ctx):
    """
    Uppercase name for each member
    """
    guild = utils.get(bot.guilds, id=gnp_guild_id)
    task_list = []
    for member in [ member for member in guild.members if member.top_role.name == "member"]:
        ## Edit nickname to upper case
        if member.display_name.lower() != member.display_name:
            try:
                task_list.append(
                    asyncio.create_task(member.edit(nick=member.display_name.lower()))
                )
            except Exception as e:
                pass

    for task in task_list:
        await task
    await ctx.message.add_reaction("👍")

@bot.command()
@commands.has_permissions(administrator=True)
async def memberall(ctx):
    """
    Search for non-member people, append member role to them
    """
    role = utils.get(ctx.guild.roles, name="member")
    for member in [i for i in ctx.guild.members if not i.bot]:
        if not 'member' in [role.name for role in member.roles]:
            await member.add_roles(role)

    await ctx.message.add_reaction("👍")

@bot.command()
async def test(ctx):
    """
    tu record from Mudae db
    """
    msg = await ctx.channel.fetch_message(965801395607453766)
    await ctx.send(
        embed=msg.embeds[0]
    )

@bot.command()
async def tu(ctx):
    """
    tu record from Mudae db
    """
    await ctx.send(
        str(MudaeTuRecord(ctx.author.name, from_db=True))
    )

@bot.command()
async def roles(ctx, *, member: MemberRoles = None):
    """
    Shows a member's roles.
    * means next arguments will be named args
    """

    if member:
        await ctx.send('I see the following roles: **{}**'.format('**, **'.join(member)))
        return
    await ctx.send('I see the following roles: **{}**'.format('**, **'.join([str(i) for i in ctx.author.roles[1:]]))) # [1:] removes everyone role

@bot.command()
@only_for_user(user_list["mondo"])
async def shabi(ctx, *, member: Member = None):
    """
    Prepends SHABI to the display name of given member
    """
    if not member:
        return

    ## Do not change bots names
    if member.bot:
        return

    try:
        if not "SHABI" in member.display_name:
            new_nick = "SHABI "+member.display_name
            await member.edit(nick=new_nick)
        await ctx.message.add_reaction("👍")

    except Exception as e:
        await ctx.message.add_reaction("😥")

@bot.command()
@only_for_user(user_list["redguard"])
async def unshabi(ctx, *, member: Member = None):
    """
    Prepends SHABI to the display name of given member
    """
    if not member:
        return

    ## Do not change bots names
    if member.bot:
        return

    try:
        if "SHABI " in member.display_name:
            new_nick = member.display_name.replace("SHABI ", "")
            await member.edit(nick=new_nick)
        await ctx.message.add_reaction("👍")

    except Exception as e:
        await ctx.message.add_reaction("😥")

@bot.command(name="mute", aliases=["m"])
@commands.has_permissions(administrator=True)
@guild_only(gnp_guild_id) # Works for gnp server only
async def mute(ctx, *, member: Member):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role =   utils.get(ctx.guild.roles, id=912781839633096734)
    member_role = utils.get(ctx.guild.roles, id=912783144015528016)

    await member.add_roles(mute_role)
    await member.remove_roles(member_role)
    await ctx.send('**{}** is muted'.format(member.display_name))

@bot.command(name="muted_members", aliases=["mm"])
@commands.has_permissions(administrator=True)
@guild_only(gnp_guild_id) # Works for gnp server only
async def muted_members(ctx):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role =   utils.get(ctx.guild.roles, id=912781839633096734)
    member_role = utils.get(ctx.guild.roles, id=912783144015528016)

    await ctx.message.add_reaction("👍")
    print(
        '\n'.join(
            ['Roles: {roles_color}{roles}{nocolor} for Member: {member_color}{member}{nocolor}'.format(
                roles = ', '.join([str(i) for i in member.roles]),
                member = member.name,
                roles_color = COLOR_YELLOW,
                member_color = COLOR_RED,
                nocolor = COLOR_END
             )
             for member in ctx.guild.members]
        )
    )

@bot.command(name="unmute", aliases=["um"])
@commands.has_permissions(administrator=True)
@guild_only(gnp_guild_id) # Works for gnp server only
async def unmute(ctx, *, member: Member):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role =   utils.get(ctx.guild.roles, id=912781839633096734)
    member_role = utils.get(ctx.guild.roles, id=912783144015528016)

    await member.add_roles(member_role)
    await member.remove_roles(mute_role)
    await ctx.send('**{}** is unmuted'.format(member.display_name))


@bot.command(name="avatar", aliases=["pp", "pfp"])
async def avatar(ctx, *, member: Member = None):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    if member:
        await ctx.message.reply('{}'.format(member.avatar.url))
        return

    await ctx.message.reply('{}'.format(ctx.author.avatar.url))

@bot.command(name="emojis", aliases=["emoji"])
async def emojis(ctx):
    """
    Guild emojis
    """
    await ctx.send(
        '{}'.format(
            '\n'.join(
                ["{} :{}:".format(
                    utils.get(ctx.guild.emojis, id=emoji.id),
                    emoji.name)
                 for emoji in
                 sample(
                     [i for i in ctx.guild.emojis if i.available],
                     9
                 )
                 ]
            )
        )
    )

@bot.command(name="randreact", aliases=["rreact", "rr"])
async def randreact(ctx):
    """
    React with random guild emojis
    """

    message = await ctx.channel.history(limit=2).flatten()
    message = message[1]
    await ctx.message.delete()

    available_emojis = [i for i in ctx.guild.emojis if i.available]
    random_emojis = sample(available_emojis, 9)

    await gather(*[
            message.add_reaction(emoji) for emoji in random_emojis
        ])


# Command Homuri
bot.command(name="homuri")(name)

# Command Ping
bot.command()(ping)

## Run
bot.run(TOKEN)
