import discord
from discord.ext import commands
import os
from .constant import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # in order to access the messages

# commands with '&' prefix is used to call the bot for specific operation
client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f"{extension} module has been loaded")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    await client.unload_extension(f'src.cogs.{extension}')
    await ctx.send(f"{extension} module has been unloaded")


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    await client.unload_extension(f'src.cogs.{extension}')
    await client.load_extension(f'src.cogs.{extension}')
    await ctx.send(f"{extension} module has been reloaded")


@client.command()
@commands.is_owner()
async def unload_all(ctx):
    for file in os.listdir('src/cogs/'):
        if file.endswith('.py'):
            try:
                await client.unload_extension(f'src.cogs.{file[:-3]}')
                print(f'Loaded {file}')
            except Exception as e:
                print(f'Failed to load {file}: {e}')

    await ctx.send(f"All module has been unloaded")

@client.command()
@commands.is_owner()
async def load_all(ctx):
    try:
        for file in os.listdir('src/cogs/'):
            if file.endswith('.py'):
                try:
                    await client.load_extension(f'src.cogs.{file[:-3]}')
                    print(f'Loaded {file}')
                except Exception as e:
                    print(f'Failed to load {file}: {e}')
        await ctx.send(f"All modules have been loaded")
    except commands.NotOwner:
        await ctx.send("You need to be the owner to use this command.")


@client.event
async def on_ready():
    for file in os.listdir('src/cogs/'):
        if file.endswith('.py'):
            try:
                await client.load_extension(f'src.cogs.{file[:-3]}')
                print(f'Loaded {file}')
            except Exception as e:
                print(f'Failed to load {file}: {e}')
                
@client.event
async def on_command(ctx: commands.context):
    print(color.YELLOW + f'Command:{COMMAND_PREFIX}{ctx.command}' + color.END)
    print(color.CYAN + f'Command arguments: {ctx.kwargs}' + color.END)
    print(color.CYAN + f'executed by {ctx.author}' + color.END)
    
@client.event
async def on_command_error(ctx: commands.context, error:commands.CommandError):
    print(color.RED + f'Command:{COMMAND_PREFIX}{ctx.command}' + color.END)
    print(color.CYAN + f'Command arguments: {ctx.kwargs}' + color.END)
    print(color.CYAN + f'executed by {ctx.author}' + color.END)
    print(color.CYAN + f'Error {error}' + color.END)