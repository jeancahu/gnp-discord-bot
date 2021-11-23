# GNP Bot

from discord.ext import commands
from sys import exit
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
bot = commands.Bot(command_prefix="h>")
logs_channel =  bot.get_channel(912781470668582962)
bot.remove_command("help")

def on_ready():
    print("Bot is online")

@bot.listen()
async def on_command(message):
    if message.author.id == 863062654699438110: # Bot itself
        return

    if message.author.id == white_list[0]: # Bayonetta
        await logs_channel.send("Bayonetta: {}".format(message.content))
        return

    if message.author.id == 654134051854352404: # Samus
        await logs_channel.send("Samus: {}".format(message.content))
        return

    await AntiScam(message, bot = bot, whitelist = white_list, muted_role='Muted', verified_role='member', logs_channel=logs_channel)

@bot.command(name="homuri")
async def name(ctx):
    await ctx.send(f"{ctx.author.mention} hello uwu")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

## Run
on_ready()
bot.run(TOKEN)
