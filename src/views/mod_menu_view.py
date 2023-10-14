import discord
from src.views.create_challenge import ViewChannels
from discord.ext import commands


class ModMenuView(discord.ui.View):
    ctx: commands.context

    def __init__(self, ctx: commands.context):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(label="Create Challenge", row=0, style=discord.ButtonStyle.primary)
    async def create_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.style = discord.ButtonStyle.gray
        await self.ctx.send('', view=ViewChannels(self.ctx))
        await interaction.response.edit_message(view=self)
