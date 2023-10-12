from typing import Any

import discord
from datetime import datetime, timedelta, timezone

from discord import Interaction
from discord._types import ClientT

from src.database.parse_url import parse_hashtags
from src.database.user_data import ChallengeDetails, UserPostUpdate


class EndChallengeDropDown(discord.ui.Select):
    def __init__(self, ctx):
        self.server_id = ctx.guild.id
        self.user_id = ctx.author.id

        self.challenge_details = ChallengeDetails(server_id=self.server_id)

        # dict of challenges and challenge_id
        self.challenges_from_db = self.challenge_details.get_challenges()

        # list of challenges
        self.challenges_list = self.challenges_from_db.keys()

        options = [discord.SelectOption(label=challenge) for challenge in self.challenges_list]

        super().__init__(placeholder="Choose the challenge to post update", options=options)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:

        UserChallenge_check = UserPostUpdate(
            server_id=self.server_id,
            user_id=self.user_id
        )

        # accessing challenge_id using challenge name
        challenge_id = self.challenges_from_db[self.values[0]]

        already_joined = UserChallenge_check.is_user_enrolled_and_active(challenge_id=challenge_id)

        if already_joined['enrolled']:

            if already_joined['active'] == "active":

                # changing status to inactive
                UserChallenge_check.change_status(challenge_id=challenge_id)

                # if already joined user cannot join again
                embed = discord.Embed(title="End Challenge", color=discord.Colour.red())
                embed.add_field(name=f"",
                                value=f"{interaction.user.name}, You have opted to end **{self.values[0]}** challenge."
                                      f"You will no longer be eligible to post updates regarding this challenge")
                await interaction.response.send_message("", embed=embed)
            else:
                embed = discord.Embed(title=interaction.user.name, color=discord.Colour.blue())
                embed.add_field(name=f"",
                                value=f"You have already ended this challenge")

                await interaction.response.send_message("", embed=embed)

        else:
            # if not joined the challenge cannot post update
            embed = discord.Embed(title=interaction.user.name, color=discord.Colour.red())
            embed.add_field(name=f"",
                            value=f"You have not enrolled for **{self.values[0]}** challenge, "
                                  f"and you will not be able to end this")

            await interaction.response.send_message("", embed=embed)


class EndChallengeView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(EndChallengeDropDown(ctx))
