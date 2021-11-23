# GNP Bot

from discord.ext import commands
from sys import exit

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
bot.remove_command("help")

def on_ready():
    print("Bot is online")

@bot.event
async def on_message(message):
    if message.content.startswith('homuri'):
        channel = message.channel
        await channel.send('Hello!')

@bot.listen()
async def on_command(message):
    pass

@bot.command(name="homuri")
async def name(ctx):
    await ctx.send(f"{ctx.author.mention} hello uwu")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

## Run
on_ready()
bot.run(TOKEN)
