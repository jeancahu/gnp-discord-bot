# GNP Bot

import discord
from discord.ext import commands
from sys import exit
from time import sleep
from random import choice
from AntiScam import AntiScam

try:
    TOKEN = open("TOKEN").readline().replace('\n','')
except Exception as e:
    print(e)
    exit(1)

if not TOKEN:
    exit(2)

white_list = [
    649724009243738122, # Bayonetta
    650633031064879125, # Homura
    720994385382080552, # Matler
]

fotos_samus = [
    "https://cdn.discordapp.com/attachments/663632517760286721/912942124880777267/bf9a5e34e0ed726d100e96b5a9ecbb41.png",
    "https://cdn.discordapp.com/attachments/663632517760286721/912942199535198228/PXL_20211029_171006493.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/912942199870734406/c611209542819b6097fecc8c4b125869.png",
    "https://cdn.discordapp.com/attachments/663632517760286721/913130119223185469/29472957_1555896997793329_4544933610943152128_o.jpg",
]


bot = commands.Bot(command_prefix="h>")
log_channel = None
bot.remove_command("help")

async def on_ready():
    print("Bot is online")
    log_channel = bot.get_channel(912781470668582962) # FIXME

async def on_message(message):
    if not message.guild.id == 699053837360824414: # Works for gnp server only
        return

    if message.author.id == 863062654699438110: # Bot itself
        return

    ## General logic
    log_channel = bot.get_channel(912781470668582962) # Log channel

    if message.author.id == white_list[0]: # Bayonetta
        await log_channel.send("Bayonetta: {}".format(message.content))
        return

    if message.author.id == 654134051854352404: # Samus
        await log_channel.send("Samus: {}".format(message.content))
        return

    await AntiScam.AntiScam(message, bot=bot, white_list = white_list, muted_role='Muted', verified_role='member', logs_channel=log_channel)

@bot.command(name="homuri")
async def name(ctx):
    if not ctx.guild.id == 699053837360824414: # Works for gnp server only
        return

    await ctx.send("{} hello uwu".format(ctx.author.mention))

@bot.command()
async def ping(ctx):
    if not ctx.guild.id == 699053837360824414: # Works for gnp server only
        return

    await ctx.send("pong")

@bot.command()
async def samus(ctx):
    if not ctx.guild.id == 699053837360824414: # Works for gnp server only
        return

    embed=discord.Embed(
        title="Samus",
        description='Puertorrican papi',
        color=0x6600a1)
    embed.set_image(
        url=fotos_samus[0]
    )
    embed.set_footer(text = "Love you {}".format("baby"))

    message = await ctx.send("can we skip to the good part?")
    sleep(1)
    await message.delete()

    message = await ctx.send(embed=embed)

    for foto in fotos_samus[1:]:
        sleep(0.9)
        embed.set_image(
            url=foto
        )
        await message.edit(embed=embed)

    sleep(0.9)
    await message.delete()

## Run
bot.add_listener(on_ready)
bot.add_listener(on_message, "on_message")
bot.run(TOKEN)
