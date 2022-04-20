from discord import Embed, Member, Intents, utils
from discord.ext import commands
from inspect import getmembers

from time import sleep

## Discord bot initialization
intents = Intents.default()
intents.members = True
mudae_id = 432610292342587392 # Mudae
rem_emoji_id = 847502744176820256
ram_emoji_id = 847502746025459792

client = commands.Bot(command_prefix=".", intents=intents, self_bot=True, help_command=None, case_insensitive=True)

try:
    TOKEN = open("TOKEN_selfbot").readline().replace('\n','')
except Exception as e:
    print(e)
    exit(1)

if not TOKEN:
    exit(2)


async def on_ready():
    print("Self-bot is online")
    channel_bots = client.get_channel(820831827736395816) # Nabots
    channel_dank = client.get_channel(820830621298327583) # Dank memer
    channel_trtl = client.get_channel(794951628721487882) # Turtle
    channel_anim = client.get_channel(797876488133148693) # Anime

    # Wait 6 seconds and get last 200 messages
    sleep(3)
    messages = await channel_bots.history(limit=25).flatten() +\
        await channel_dank.history(limit=25).flatten() +\
        await channel_trtl.history(limit=25).flatten() +\
        await channel_anim.history(limit=25).flatten()
    sleep(3)

    for message in [ m for m in messages if m.author.id == mudae_id ]: # Filter for mudae messages only
        for reaction in message.reactions:
            # Already claimed by me
            if reaction.me:
                continue

            # Filter non ram/rem reactions
            try:
                if reaction.emoji.id == rem_emoji_id or \
                   reaction.emoji.id == ram_emoji_id:
                    continue
            except AttributeError as e: # Emoji is a string
                continue

            # No kakera related
            if not "kakera" in str.lower(str(reaction.emoji)):
                continue

            ## React with kakera
            await message.add_reaction(reaction.emoji)
    await client.close()

## Run
client.add_listener(on_ready)
client.run(
    TOKEN,
    bot=False)
