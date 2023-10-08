from discord.ext import commands
from src.views.user_start_challenge import *
from src.views.user_post_update import *


class StartChallenge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    @commands.command()
    async def StartChallenge(self, ctx):
        await ctx.send(view=ChallengesList(server_id=ctx.guild.id,
                                           user_id=ctx.author.id))

    @commands.command()
    async def PostUpdate(self, ctx):
        await ctx.send("Choose the challenge you want to update the post for",
                       view=UpdateModal(server_id=ctx.guild.id,
                                           user_id=ctx.author.id))


async def setup(client):
    await client.add_cog(StartChallenge(client))
