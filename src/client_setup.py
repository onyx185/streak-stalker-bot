import discord
from discord.ext import commands


"""
this file includes all setup configuration
"""


def setup_configure():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True  # in order to access the messages

    # commands with '$' prefix is used to call the bot for specific operation
    return commands.Bot(command_prefix='$', intents=intents)


client = setup_configure()


@client.event
async def on_ready():
    print(f'{client.user} is now running')
    print('--------------------------------')

