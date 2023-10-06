from src.client_setup import client
import discord
from discord.ext import commands

"""
add all the commands which has to be handled by the bot in this module.

use ${name of the command} to invoke command in the server
"""

@client.command()
async def user_info(ctx, member: discord.Member = None):

    if member == None:
        member = ctx.message.author

    embed = discord.Embed(
        title="User Info",
        description="Users status",
        color=discord.Colour.green(),  # Pycord provides a class with default colors you can choose from
    )

    embed.set_thumbnail(url = member.avatar)
    embed.add_field(name="ID",value=member.id)
    embed.add_field(name="Name", value=member.name)
    embed.add_field(name="Joined", value=member.joined_at)
    embed.add_field(name="Streak", value=15)
    embed.add_field(name="Eligibility", value="Not Eligible")

    await ctx.send("", embed=embed)

@client.command()
@commands.has_any_role("Administrators")
async def menu(ctx, member: discord.Member = None):
    try: 
        print("menu")
    except x:
        print("no role")