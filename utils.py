from math import modf as fract
from time import time
from discord import utils

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

def print_colors(guild):
    roles_str = "Name: {}, Color: {}"
    roles = [roles_str.format(role.name, role.color) for role in guild.roles if not
             role.is_default() and not
             role.is_bot_managed() and not
             role.hoist and not
             role.is_premium_subscriber() and not
             str(role.color) == "#ffffff" and
             6442450944 == role.permissions.value
             ]

    print("\n".join(roles))

def print_member_list(guild):
    member_list = []
    for member in [ member for member in guild.members if not member.bot ]:

        if len(member.display_name) > 7:
            format_tabs = "\t" * 3
        elif len(member.display_name) > 15:
            format_tabs = "\t" * 2
        elif len(member.display_name) > 23:
            format_tabs = "\t" * 1
        else:
            format_tabs = "\t" * 4

        format_str = "{}\tName: {}" + format_tabs + "Color: {}\tTop role: {}\tName len: {}\tUpper: {}\tStatus: {},{},{}"

        member_list.append(
            format_str.format(
                member.id,
                member.display_name,
                member.color,
                [role.name for role in member.roles if role.name in ["member", "ADMN"] ][-1],
                len(member.display_name),
                member.display_name.upper(),
                member.mobile_status,
                member.desktop_status,
                member.web_status
            )
        )

    member_str = "\n".join(member_list)
    print(member_str)

def if_zoo_print(message):
    if not "zoo!" in message.content:
        return False

    content = message.content
    tiny_digits = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    animals = [
        ["🐝", "bee"],
        ["🐛", "worm"],
        ["🐌", "snail"],
        ["🐞", "ladybug"],
        ["🦋", "butterfly"],
        ["🐤", "chick"],
        ["🐁", "rat"],
        ["🐓", "chicken"],
        ["🐇", "bunny"],
        ["🐿", "squirrel"],
        ["🐑", "sheep"],
        ["🐖", "pig"],
        ["🐄", "cow"],
        ["🐕", "dog"],
        ["🐈", "cat"],
        ["🐊", "alligator"],
        ["🐅", "tiger"],
        ["🐧", "penguin"],
        ["🐘", "elephant"],
        ["🐳", "whale"],
        ["🐉", "dragon"],
        ["🦄", "unicorn"],
        ["☃", "snowman"],
        ["👻", "ghost"],
        ["🕊", "dove"],
        ["<a:gdeer:418290217989046274>", "deer"],
        ["<a:gfox:418291892376305664>", "fox"],
        ["<a:glion:418289164736528404>", "lion"],
        ["<a:gowl:418284974593277954>", "owl"],
        ["<a:gsquid:417968419984375808>", "squid"]
    ]
    for i in range(10):
        content = content.replace(tiny_digits[i], str(i))

    content = content.split("\n")[1:-2]
    temp = []
    result = []
    for line in content:
        temp += \
            [ value for value in line.split(' ')[1:] if len(value) ]

    for line, animal in zip(temp[:len(animals)], animals):
        new_line = line.replace(animal[0], animal[1] + " " ).split(" ")

        if int(new_line[1]):
            result.append(" ".join(new_line))

    print("owo sacrifice " + "\nowo sacrifice ".join(result))
    return True

async def compute_for_owo(message):
    if_zoo_print(message)

    if message.channel.id == 699053838040039557: # General GNP in GNP guild
        nabots_channel = utils.get(message.guild.text_channels, id=820831827736395816) # nabots
        nabs_gaes_channel = utils.get(message.guild.text_channels, id=699053838040039557) # gaenabs

        if "Here is your daily" in message.content or "You need to wait" in message.content:
            await nabots_channel.send("OwO said:\n{}\nOn {} channel.".format(message.content, nabs_gaes_channel.name))
            await message.delete()
            return

        embeds = getattr(message, "embeds")
        if len(embeds):
            if "Here is the list of commands" in message.embeds[0].description:
                await nabots_channel.send(embeds=message.embeds)
                await message.delete()
                return

async def compute_for_nonbots(message):
    if message.channel.id == 699053838040039557: # General GNP in GNP guild

        content = message.content.lower()
        content = [ i for i in content.split(' ') if i ]

        if content[0] == "owo":
            if content[1] == "daily" or "help":
                nabots_channel = utils.get(message.guild.text_channels, id=820831827736395816) # nabots

                await nabots_channel.send("{}".format(message.author.mention))
                await message.delete()
