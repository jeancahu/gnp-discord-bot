# GNP Bot

from discord import Embed, Member, Intents, utils # Bot TODO
from discord import __version__ as discord_version
from discord.ext import commands # it's no needed for 1.7.3> # TODO (Change on 1.7.3 release)

import paho.mqtt.client as mqtt

from sys import exit
from time import sleep, time
from random import choice, sample
from AntiScam import AntiScam

from asyncio import gather

from commands import ping, name
from constants import white_list, fotos_samus, bayo_images

import re

from inspect import getmembers # TODO Remove
from mudae import MudaeTuRecord, MudaeClaimEmbed

import signal

def handler_stop_signals(signal, frame):
    print("Good bye!")
    exit(0)

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

## Users list
samus = (654134051854352404, "Samus")
bayo = (649724009243738122, "Nabonetta")

guild_id = 699053837360824414 # GNP

## Decorators
def guild_only(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

def only_for_user(user_id, user_name): # Functions who returns a decorator
    async def predicate(ctx):
        if not ctx.author.id == user_id:
            await ctx.send("Hey tú no eres {}!".format(user_name))
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

bot = commands.Bot(command_prefix="h>", intents=intents, case_insensitive=True)
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

async def on_ready():
    print("Bot is online, Pycord version: {}".format(discord_version))

@guild_only(guild_id) # Works for gnp server only
async def on_message(message):
    global mqtt_enable
    if message.author.id == 863062654699438110: # Bot itself
        return

    try:
        # Init a mudae $tu record object
        if message.author.id == 432610292342587392: # Mudae Bot
            mudae_tu_record_temp = MudaeTuRecord(message)
            mudae_tu_record_temp.save()
            return
    except ValueError as e:
        pass
        # print("\tError: {}".format(e))
    except TypeError as e:
        pass
        # print("\tError: {}".format(e))

    if message.author.id == 432610292342587392: # Mudae Bot
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
                ##print(getmembers(message)) ## FIXME remove

        except Exception as e: # There is not Embed
            pass
            # print("Mudae BOT (except {}): {}".format(e, message.content))
        return

    ## AntiScam # TODO fix false positive
    ## await AntiScam.AntiScam(message, bot=bot, white_list = white_list, muted_role='Muted', verified_role='member', logs_channel=None)

async def on_reaction_add(reaction, user):
    if user.id == 863062654699438110: # Bot itself
        return

    try:
        # Init a mudaeClimEmbed record object
        mudae_claim_embed_temp = MudaeClaimEmbed(reaction=reaction, user=user)
        # return
    except ValueError as e:
        pass
    except TypeError as e:
        pass

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
    Tells you a member's roles.
    * means next arguments will be named args
    """
    if member:
        await ctx.send('I see the following roles: **{}**'.format('**, **'.join(member)))
        return
    await ctx.send('I see the following roles: **{}**'.format('**, **'.join([str(i) for i in ctx.author.roles[1:]]))) # [1:] removes everyone role

@bot.command()
async def member(ctx, *, member: Member):
    """
    Tells you a member's name.
    * means next arguments will be named args
    """
    await ctx.send('**{}**'.format(member))

@bot.command(name="mute", aliases=["m"])
@commands.has_role("ADMN")
@guild_only(guild_id) # Works for gnp server only
async def mute(ctx, *, member: Member):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role = ctx.guild.get_role(912781839633096734)
    member_role = ctx.guild.get_role(912783144015528016)

    await member.add_roles(mute_role)
    await member.remove_roles(member_role)
    await ctx.send('**{}** is muted'.format(member.name))

@bot.command(name="muted_members", aliases=["mm"])
@commands.has_role("ADMN")
@guild_only(guild_id) # Works for gnp server only
async def muted_members(ctx):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role = ctx.guild.get_role(912781839633096734)
    member_role = ctx.guild.get_role(912783144015528016)

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
@commands.has_role("ADMN")
@guild_only(guild_id) # Works for gnp server only
async def unmute(ctx, *, member: Member):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role = ctx.guild.get_role(912781839633096734)
    member_role = ctx.guild.get_role(912783144015528016)

    await member.add_roles(member_role)
    await member.remove_roles(mute_role)
    await ctx.send('**{}** is unmuted'.format(member.name))


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
    available_emojis = [i for i in ctx.guild.emojis if i.available]
    random_emojis = sample(available_emojis, 9)

    await gather(*[
            message.add_reaction(emoji) for emoji in random_emojis
        ])
    await ctx.message.delete()

# Command Homuri
bot.command(name="homuri")(name)

# Command Ping
bot.command()(ping)

## Run
bot.add_listener(on_ready)
bot.add_listener(on_message, "on_message")
bot.add_listener(on_reaction_add, "on_reaction_add")
bot.run(TOKEN)
