import discord
from discord.ext import commands


class CreateChallenge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    @commands.command()
    async def Create(self, ctx):
        await ctx.send("Hello")

    @commands.command()
    async def Edit(self, ctx):
        await ctx.send("Hello")

    @commands.command()
    async def Delete(self, ctx):
        await ctx.send("Hello")

    @commands.command()
    async def ViewParticipants(self, ctx):
        await ctx.send("Hello")



async def setup(client):
    await client.add_cog(CreateChallenge(client))



