async def ping(ctx):
    """
    Ping command to verify bot is online
    """
    await ctx.send("pong")

async def name(ctx):
    """
    Reply a mention to the command message author
    """
    await ctx.send("{} hello uwu".format(ctx.author.mention))

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
