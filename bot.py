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
logs_channel = 912781470668582962

bot = commands.Bot(command_prefix="h>")
bot.remove_command("help")

def on_ready():
    print("Bot is online")

@bot.listen()
async def on_command(message):
    if message.author.id == 863062654699438110: # Bot itself
        return

    await AntiScam(message, bot = bot, whitelist = whitelist, muted_role='Muted', verified_role='member', logs_channel=logs_channel)

    if message.content.startswith('homuri'):
        channel = message.channel
        await channel.send('Hello!')

@bot.command(name="homuri")
async def name(ctx):
    await ctx.send(f"{ctx.author.mention} hello uwu")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

## Run
on_ready()
bot.run(TOKEN)
