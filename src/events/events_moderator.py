from src.client_setup import client

"""
add all the events which has to be handled by the bot in this module
"""


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_message = str(message.content)
    username = str(message.author)
    channel = str(message.channel)

    if user_message.startswith('$'):
        await client.process_commands(message)
    else:
        await message.channel.send(username + ' said: ' + user_message + ' in ' + channel)


@client.event
async def on_member_join(member):
    channel = member.guild.system_channel  # Get the system channel of the guild
    username = member.name
    isBot = member.bot

    if channel is not None:
        await channel.send(f'Welcome to the server, {member.mention}!')
