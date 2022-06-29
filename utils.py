from math import modf as fract
from time import time

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
