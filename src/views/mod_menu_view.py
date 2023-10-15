import discord
from discord.ext import commands
from src.views.create_challenge import ViewChannels
from src.database.get_stats import get_stats
import io
import base64

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

    @discord.ui.button(label="Get Stats", row=0, style=discord.ButtonStyle.secondary)
    async def get_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:      
            button.disabled = True
            button.style = discord.ButtonStyle.gray
            await interaction.response.edit_message(view=self)
            serverId = interaction.guild_id
            response = get_stats(serverId)
            file = discord.File(io.BytesIO(base64.b64decode(response)), 'stats.png')
            return await self.ctx.send(file=file)
        except Exception as e:
            await self.ctx.send('Something went wrong, try again.')
