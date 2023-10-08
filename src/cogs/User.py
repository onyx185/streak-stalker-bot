from discord.ext import commands
from src.views.User_ui import *


class StartChallenge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    @commands.command()
    async def StartChallenge(self, ctx):
        await ctx.send(view=ChallengesList())

    @commands.command()
    async def PostUpdate(self, ctx):
        await ctx.send(view=UpdateModal())


async def setup(client):
    await client.add_cog(StartChallenge(client))
