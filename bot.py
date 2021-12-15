# GNP Bot

import discord
from discord.ext import commands
from sys import exit
from time import sleep, time
from random import choice
from AntiScam import AntiScam
from math import modf as fract
from functools import wraps

## Util functions
def mins_hours_until (seconds):
    minutes, hours = fract((seconds - time())/(60*60))
    return (int(minutes*60), int(hours))

def cooldown_message (cooldown):
    minutes, hours = mins_hours_until(cooldown)
    if hours:
        return "Debes esperar **{}** horas con **{}** minutos de cooldown".format(
            hours,
            minutes
        )

    return "Debes esperar **{}** minutos de cooldown".format(
        minutes
    )

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

white_list = [
    649724009243738122, # Bayonetta
    650633031064879125, # Homura
    720994385382080552, # Matler
]

fotos_samus = [
    # cabrito
    "https://media.discordapp.net/attachments/686816510710120483/836615939965452298/photo_2021-04-24_18-55-13.jpg?width=748&height=561",
    "https://media.discordapp.net/attachments/686816510710120483/842208208096591902/photo_2021-05-12_19-13-44.jpg?width=997&height=561",
    "https://media.discordapp.net/attachments/686816510710120483/911457815468597248/unknown.png?width=748&height=561",
]

bayo_images = [
    "https://cdn.discordapp.com/attachments/663632517760286721/920540272725733396/530c773218db6a7d39bc953bdc1e6447.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544001273233459/FB_IMG_1635188932987.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544076347105300/FB_IMG_1635188927363.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544136317239306/0a15d1e1bed0bf2d7edb6b41160007d3.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544169766830102/FB_IMG_1634879081357.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544222275338261/1764441631c58cd5321f7736aa17901f.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544292148236308/1415103660_212416_1532530600_miniatura_normal.png",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544320669499432/4825c353bebff737bf94ac17c80e5955.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544530690875392/FB_IMG_1615818564276.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544610583994418/Bayonettaanarchyreigns.png",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544610911125534/2a8987419e9002f8948e7709b0799abe.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544611125043270/f8b08b69bb5d810f47709b6852d0f328.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544741207179314/0252bf8753d1f5e8271f131bade17565.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544741458862101/d8c38814e5e2666d5a6fcc21add6ad66.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544742213840957/fb308409d7903101c5c1f4f8f5766759.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544742691971102/e9bfc5ac91270054a7d44506aa4f2005.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544895997976637/FB_IMG_1606537078954.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544896337739806/FB_IMG_1606537075137.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544896698417242/FB_IMG_1605114798329.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544897025581096/FB_IMG_1589423993137.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920544897256263742/7901e7c379b031034c5156b8b2f95746.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920545006576631828/fbfb2ba555d422d0d293d2a5a071dc57.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920545006886989824/9d0dfda8a53e7cb4fb45cf95ba7c3eb0.jpg",
    "https://cdn.discordapp.com/attachments/663632517760286721/920545007142850621/8011499df779cea3a73b0a27c246b105.jpg",
]

## Global variables
bot = commands.Bot(command_prefix="h>")
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

@bot.command(name="homuri")
async def name(ctx):
    await ctx.send("{} hello uwu".format(ctx.author.mention))

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

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
