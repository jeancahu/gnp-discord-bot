# GNP Bot

import discord
from discord.ext import commands
from sys import exit
from time import sleep, time
from random import choice
from AntiScam import AntiScam
from functools import wraps

from commands import ping, name
from utils import mins_hours_until, cooldown_message
from constants import white_list, fotos_samus, bayo_images

## Users list
samus = (654134051854352404, "Samus")
bayo = (649724009243738122, "Nabonetta")

## Decorators

def guild_only(func): # A decorator
    @wraps(func)
    async def f_wrapper(ctx):
        if not ctx.guild.id == 699053837360824414: # Works for gnp server only
            return
        return await func(ctx)

    return f_wrapper

def only_for_user(user_id, user_name): # Functions who returns a decorator
    def out_decorator(func):
        @wraps(func)
        async def f_wrapper(ctx):
            if not ctx.author.id == user_id:
                await ctx.send("Hey tú no eres {}!".format(user_name))
                return
            return await func(ctx)
        return f_wrapper

    return out_decorator

try:
    TOKEN = open("TOKEN").readline().replace('\n','')
except Exception as e:
    print(e)
    exit(1)

if not TOKEN:
    exit(2)

## Global variables
bot = commands.Bot(command_prefix="h>", case_insensitive=True)
log_channel = None
bot.remove_command("help")
protection = time() + 8*60*60 # Time until we can use command again
protection_cooldown = 0

div_cooldown = 0 # Time until we can use command again
steal_cooldown = 0 # Time until we can use command again
esama_cooldown = 0

async def on_ready():
    print("Bot is online")
    log_channel = bot.get_channel(912781470668582962) # FIXME

@guild_only
async def on_message(message):
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

async def on_reaction_add(reaction, user):
    if user.id == 863062654699438110: # Bot itself
        return
    #print(user.name)
    pass

# Command Homuri
bot.command(name="homuri")(name)

# Command Ping
bot.command()(ping)

# Command Defme
@bot.command()
@guild_only
@only_for_user(user_id=samus[0], user_name=samus[1])
async def defme(ctx):
    global protection
    global protection_cooldown

    if protection_cooldown > time():
        embed=discord.Embed(
            title="Homura no tiene energía",
            description=cooldown_message(protection_cooldown),
            color=0x6600a1)
        embed.set_image(
            url="https://vigarathtalks.files.wordpress.com/2014/07/tumblr_n388p3c4e11r2heyno2_500.gif"
        )
        embed.set_footer(text = "No he logrado defenderte...")
        message = await ctx.send(embed=embed)
        return

    protection = time() + 8*60*60 # protection for 8 hours
    await ctx.send("Estás protegido por **8** horas a partir de ahora bebé")

@bot.command()
@guild_only
@only_for_user(user_id=bayo[0], user_name=bayo[1])
async def bayo(ctx):
    image = choice(bayo_images)
    await ctx.send(image)

@bot.command()
async def whoissus(ctx):
    await ctx.send("<@330030494534336512>, he is sus af")

@bot.command()
async def sus(ctx):
    await ctx.send("<@330030494534336512>, he is sus af 🦃")

@bot.command()
async def tg(ctx):
    embed=discord.Embed(
        title="This is The Goat",
        description='New profile picture',
        color=0x6600a1)
    embed.set_image(
        url='https://cdn.discordapp.com/attachments/861388324597399584/921457215452373052/masked.png'
    )
    embed.set_footer(text = "basically, he is sus af")
    message = await ctx.send(embed=embed)

@bot.command()
@guild_only
async def div(ctx):
    global protection
    global div_cooldown

    # Cooldown

    if div_cooldown > time():
        await ctx.send(
            cooldown_message(div_cooldown)
        )
        return

    protection = int(time() + ((protection - time())/2))
    div_cooldown = time() + 60*60

    embed=discord.Embed(
        title="Divine dividing",
        description='Samus pierde la mitad de su poder protector',
        color=0x6600a1)
    embed.set_image(
        url='https://cdn.discordapp.com/attachments/861388324597399584/919971231351074907/latest.png'
    )
    embed.set_footer(text = "Love you {}".format("baby"))
    message = await ctx.send(embed=embed)
    # sleep(0.9)
    # await message.delete()

@bot.command()
@guild_only
async def steal(ctx):
    global protection
    global steal_cooldown

    # Cooldown

    if steal_cooldown > time():
        await ctx.send(
            cooldown_message(steal_cooldown)
        )
        return


    protection = int(protection - 60*60)
    steal_cooldown = time() + 40*60

    embed=discord.Embed(
        title="Steal",
        description='Una hora de protección es robada',
        color=0x6600a1)
    embed.set_image(
        url='https://cdn.discordapp.com/attachments/861388324597399584/919980690630647908/steal.gif'
    )
    embed.set_footer(text = "Love you {}".format("baby"))
    message = await ctx.send(embed=embed)
    # sleep(0.9)
    # await message.delete()

@bot.command()
@guild_only
async def esama(ctx):
    global protection_cooldown
    global esama_cooldown

    # Cooldown

    if esama_cooldown > time():
        await ctx.send(
            cooldown_message(esama_cooldown)
        )
        return

    protection_cooldown = int(time() + 60*60)
    esama_cooldown = time() + 60*60*3

    embed=discord.Embed(
        title="Esdeath-sama",
        description='El comando de protección queda congelado por una hora',
        color=0x6600a1)
    embed.set_image(
        url="https://i.pinimg.com/originals/68/ef/9a/68ef9a274152da8e75eccfd47343e5c4.gif"
    )
    embed.set_footer(text = "Love you {}".format("baby"))
    message = await ctx.send(embed=embed)
    # sleep(0.9)
    # await message.delete()

@bot.command()
@guild_only
async def samus(ctx):
    global protection

    if protection > time():
        sadpepe = discord.utils.get(ctx.guild.emojis, id=699096328055291995)
        message = await ctx.send(
            "Quedan **{0[1]}** horas con **{0[0]}** minutos de protección {1}".format(
                mins_hours_until(protection),
                sadpepe
            )
        )
        await message.add_reaction(sadpepe)
        return

    embed=discord.Embed(
        title="Cabrito",
        description='Cabrito wonito',
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
bot.add_listener(on_reaction_add, "on_reaction_add")
bot.run(TOKEN)
