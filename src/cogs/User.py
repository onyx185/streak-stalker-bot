from discord.ext import commands
import discord
from src.views.user_start_challenge import ChallengesList
from src.views.user_post_update import UpdateModal
from src.views.user_end_challenge import EndChallengeView
from src.database.user_data import get_servers_registered_for_challenge


class StartChallenge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    @commands.command()
    async def StartChallenge(self, ctx):
        server_has_challenge = get_servers_registered_for_challenge(ctx.guild.id)

        if server_has_challenge:
            await ctx.send(view=ChallengesList(ctx))
        else:
            embed = discord.Embed(
                title="No Challenges Found",
                color=discord.Colour.red(),  # Pycord provides a class with default colors you can choose from
            )

            embed.add_field(name=f"Oh no challenges",
                            value="This server has no challenges created.")
            await ctx.send(embed=embed)

    @commands.command()
    async def PostUpdate(self, ctx):
        server_has_challenge = get_servers_registered_for_challenge(ctx.guild.id)

        if server_has_challenge:
            await ctx.send("Choose the challenge you want to update the post for",
                           view=UpdateModal(ctx))
        else:
            embed = discord.Embed(
                title="No Challenges Found",
                color=discord.Colour.red(),  # Pycord provides a class with default colors you can choose from
            )

            embed.add_field(name=f"Oh no challenges",
                            value="This server has no challenges created. Please create challenges.")
            await ctx.send(embed=embed)

    @commands.command()
    async def EndChallenge(self, ctx):
        server_has_challenge = get_servers_registered_for_challenge(ctx.guild.id)

        if server_has_challenge:
            await ctx.send("Choose the challenge you want to end",
                           view=EndChallengeView(ctx))
        else:
            embed = discord.Embed(
                title="No Challenges Found",
                color=discord.Colour.red(),  # Pycord provides a class with default colors you can choose from
            )

            embed.add_field(name=f"Oh no challenges",
                            value="This server has no challenges created. Please create challenges.")
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(StartChallenge(client))
