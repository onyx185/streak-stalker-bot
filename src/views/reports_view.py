import io
import pandas as pd

import discord
from discord import Interaction
from discord._types import ClientT

from src.database.get_reports import GetReport
from src.database.user_data import ChallengeDetails


class ReportsDrowpDown(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        self.server_id = ctx.guild.id
        self.user_id = ctx.author.id

        self.challenge_details = ChallengeDetails(server_id=self.server_id)

        # dict of challenges and challenge_id
        self.challenges_from_db = self.challenge_details.get_challenges()

        # list of challenges
        self.challenges_list = self.challenges_from_db.keys()


        options = [discord.SelectOption(label=challenge) for challenge in self.challenges_list]
        options.insert(0, discord.SelectOption(label="All"))

        super().__init__(placeholder="Select the Challenge you want report for", options=options)

    async def callback(self, interaction: Interaction[ClientT]):
        if self.values[0] == "All":
            report_obj = GetReport(ctx=self.ctx, challenge_id=0)
        else:
            challenge_id = self.challenges_from_db[self.values[0]]['challenge_id']
            report_obj = GetReport(ctx=self.ctx, challenge_id=challenge_id)

        if report_obj.data_present:

            dataframe = report_obj.get_report()
            dataframe_user_post = report_obj.get_users_posts_details()

            try:
                user_id = dataframe['User ID'].to_list()
                user_name_all = []
                for id_ in user_id:
                    user_name = await self.ctx.guild.fetch_member(id_)
                    user_name_all.append(user_name.name)

                dataframe['Discord User Name'] = user_name_all
            except:
                pass

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, sheet_name='Report', index=False)
                dataframe_user_post.to_excel(writer, sheet_name='Users Posts', index=False)

            excel_buffer.seek(0)

            data = discord.File(excel_buffer, filename="Report.xlsx")

            await interaction.response.send_message(file=data)
        else:

            embed = discord.Embed(title="No Users data found", color=discord.Colour.dark_blue())

            await interaction.response.send_message(embed=embed)




class ReportForChallenges(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(ReportsDrowpDown(ctx))
