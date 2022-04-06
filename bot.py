# GNP Bot

from discord import Embed, Member, Intents, utils # Bot TODO
from discord import __version__ as discord_version
from discord.ext import commands # it's no needed for 1.7.3>

from sys import exit
from time import sleep, time
from random import choice, sample
from AntiScam import AntiScam

from asyncio import gather

from commands import ping, name
from utils import mins_hours_until, cooldown_message
from constants import white_list, fotos_samus, bayo_images

import re
import json

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
bot = commands.Bot(command_prefix="h>", case_insensitive=True)
bot.remove_command("help")

log_channel = None
protection = time() # + 8*60*60 # Time until we can use command again
protection_cooldown = 0

div_cooldown = 0 # Time until we can use command again
steal_cooldown = 0 # Time until we can use command again
esama_cooldown = 0

class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]] # Remove everyone role!

@bot.check
async def globally_block_dms(ctx):
    # Block DMs
    return ctx.guild is not None

async def on_ready():
    print("Bot is online, discord version: {}".format(discord_version))
    # log_channel = bot.get_channel(912781470668582962) # FIXME

@guild_only(guild_id) # Works for gnp server only
async def on_message(message):
    if message.author.id == 863062654699438110: # Bot itself
        return

    if message.author.id == 432610292342587392: # Mudae Bot
        try:
            embeds = getattr(message, "embeds")

            print("There are {} embeds.".format(len(embeds)))

            if len(embeds) == 1: # An embed only
                print("Embed on message -> Title: {}\nDescription: {}".format(json.dumps(embeds[0]), embeds[0].description))

                for field in embeds[0].fields:
                    print("Field: {}".format(field))

            else: ## Ignore embeds without title TODO
                ## Special processing for $tu output
                if "**=>** $tuarrange" in message.content:
                    ## split by newline
                    tu_lines = message.content.split('\n')
                    for line in tu_lines:
                        print("$tu command output: {}".format(line))

                    # print("User name: {}".format( re.search('^\*\*[^*]{*}\*\*', tu_lines[0]).group(0) )) # TODO
                else:
                    print("Mudae BOT: {}".format(message.content))

        except Exception as e: # There is not Embed
            print("Mudae BOT (except {}): {}".format(e, message.content))
        return

    ## AntiScam # TODO fix false positive
    ## await AntiScam.AntiScam(message, bot=bot, white_list = white_list, muted_role='Muted', verified_role='member', logs_channel=None)

async def on_reaction_add(reaction, user):
    if user.id == 863062654699438110: # Bot itself
        return

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

@bot.command(name="mute_members", aliases=["mm"])
@commands.has_role("ADMN")
@guild_only(guild_id) # Works for gnp server only
async def mute_members(ctx):
    """
    Tells you a member's roles.
    * means next arguments will be named args
    """
    mute_role = ctx.guild.get_role(912781839633096734)
    member_role = ctx.guild.get_role(912783144015528016)

    print("TODO FIXME member list muted roled")

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
