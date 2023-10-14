import discord
from src.views.create_challenge import ViewChannels
from discord.ext import commands
from src.database.get_reports import GetReport
import io
import pandas as pd


class ModMenuView(discord.ui.View):
    ctx: commands.context

    def __init__(self, ctx: commands.context):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(label="Create Challenge", row=0, style=discord.ButtonStyle.primary)
    async def create_challenge(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        button.style = discord.ButtonStyle.gray
        await interaction.response.send_message('', view=ViewChannels(self.ctx))
        # await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Get Report", row=0, style=discord.ButtonStyle.primary)
    async def get_report(self, interaction: discord.Interaction, button: discord.ui.Button):

        button.disabled = True
        button.style = discord.ButtonStyle.gray

        report_obj = GetReport(server_id=self.ctx.guild.id)

        if report_obj.data_present:

            dataframe = report_obj.get_all_report()

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, sheet_name='Sheet1', index=False)

            excel_buffer.seek(0)

            data = discord.File(excel_buffer, filename="Report.xlsx")

            await self.ctx.send(file=data)
        else:

            embed = discord.Embed(title="No Users data found", color=discord.Colour.dark_blue())

            await self.ctx.send(embed=embed)

        await interaction.response.edit_message(view=self)
