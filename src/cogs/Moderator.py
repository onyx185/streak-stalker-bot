import discord
from discord.ext import commands
from typing import List

# from views.menu_view import MenuView
from src.views.mod_menu_view import ModMenuView


class ModeratorCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    @commands.command()
    async def menu(self, ctx: commands.context):
        try:
            await ctx.send(view=ModMenuView(ctx))
        except Exception as e:
            print(e)

async def setup(client: commands.Bot):
    await client.add_cog(ModeratorCog(client))
