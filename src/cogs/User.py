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
        await ctx.send("Hello")

    @commands.command()
    async def ViewProgress(self, ctx):
        await ctx.send("Hello", view=MyView())


    # sends message to other channel
    @commands.command()
    async def modal(self, ctx):
        await ctx.send(view=ModalView())

    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(
            title="My Amazing Embed",
            description="Embeds are super easy, barely an inconvenience.",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="A Normal Field",
                        value="A really nice field with some information. **The description as well as the fields support markdown!**")

        embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
        embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
        embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)

        embed.set_footer(text="Footer! No markdown here.")  # footers can have icons too
        embed.set_author(name="Pycord Team", icon_url="https://example.com/link-to-my-image.png")
        embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
        embed.set_image(url="https://example.com/link-to-my-banner.png")

        await ctx.send("Hello! Here's a cool embed.", embed=embed)  # Send the embed with some text

    @commands.command()
    async def select(self, ctx):
        await ctx.send(view=MySelect())


async def setup(client):
    await client.add_cog(StartChallenge(client))
