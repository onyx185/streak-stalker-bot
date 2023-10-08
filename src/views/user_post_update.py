from typing import Any

import discord
from datetime import datetime, timedelta, timezone

from discord import Interaction
from discord._types import ClientT

from src.database.parse_url import parse_hashtags
from src.database.user_data import ChallengeDetails, UserPostUpdate


class PostUpdateModal(discord.ui.Modal):
    def __init__(self, username,challenge_id, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        username = username
        self.challenge_id = challenge_id

        self.all_fields = ["User Name", "Hashtags", "Social Media Links", "Message"]

        self.add_item(discord.ui.TextInput(label=self.all_fields[0], placeholder="Discord Username",
                                           default=username, required=True))
        self.add_item(discord.ui.TextInput(label=self.all_fields[1], placeholder="Enter eligible hastags",
                                           required=False))
        self.add_item(discord.ui.TextInput(label=self.all_fields[2], placeholder="Social Media Links",
                                           required=False))
        self.add_item(discord.ui.TextInput(label=self.all_fields[3], style=discord.TextStyle.long,
                                           required=False,
                                           placeholder="Your message"))

    async def on_submit(self, interaction):
        eligible_hastags = ChallengeDetails(server_id=
                                            interaction.guild_id).get_eligible_hastags(
                        challenge_id=self.challenge_id)

        data = {}
        data['discord_user'] = interaction.user.name
        data['challenge_id'] = int(self.challenge_id)
        data['discord_user_id'] = interaction.user.id
        data['submitted_in_channel'] = interaction.channel.name
        data['submited_date'] = datetime.now(tz=timezone(timedelta(hours=5, minutes=30)))

        for ind, field in enumerate(self.all_fields):
            data[field.lower().replace(" ", "_")] = interaction.data['components'][ind]['components'][0]['value']

        given_hastags = parse_hashtags(data['hashtags'])

        if (len(set(eligible_hastags).difference(set(given_hastags))))==0:
            # add record to database
            post_det = UserPostUpdate(server_id=interaction.guild_id, user_id=interaction.user.id)
            post_det.add_post_update(challenge_id=self.challenge_id, data=data)

            embed = discord.Embed(
                title="Daily Updates",
                color=discord.Colour.green(),  # Pycord provides a class with default colors you can choose from
            )

            embed.add_field(name=f"{data['discord_user']}",
                            value="Thank you for posting a update")

            await interaction.response.send_message("", embed=embed)
        else:
            embed = discord.Embed(
                title="Daily Updates",
                color=discord.Colour.red(),  # Pycord provides a class with default colors you can choose from
            )

            embed.add_field(name=f"{data['discord_user']}",
                            value="Hey, the provided hastags are not in proper format,"
                                  "User the proper hastags")

            await interaction.response.send_message("", embed=embed)

    async def on_error(self, interaction, error: Exception, /) -> None:
        print(error)


class ChallengesDropDownForPostingUpdate(discord.ui.Select):
    def __init__(self, server_id, user_id):
        self.server_id = server_id
        self.user_id = user_id

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

        already_joined = UserChallenge_check.is_user_enrolled(challenge_id=challenge_id)

        if already_joined:
            eligible_to_post = UserChallenge_check.eligible_to_post(challenge_id=challenge_id)

            if eligible_to_post:
                await interaction.response.send_modal(PostUpdateModal(username=interaction.user.name,
                                                                      challenge_id=challenge_id,
                                                                  title="Daily Updates"))
            else:
                if UserChallenge_check.kick_out:
                    # if already joined user cannot join again
                    embed = discord.Embed(title="Oops!!, You lost the Streak", color=discord.Colour.red())
                    embed.add_field(name=f"",
                                    value=f"{interaction.user.name}, Sorry you are not eligible to post update on this"
                                          f" {self.values[0]} challenge as you have lost the streak.")

                    await interaction.response.send_message("", embed=embed)
                else:
                    embed = discord.Embed(title=interaction.user.name, color=discord.Colour.blue())
                    embed.add_field(name=f"",
                                    value=f"You have already posted update for the day. Comeback tmorrow.")

                    await interaction.response.send_message("", embed=embed)

        else:
            # if not joined the challenge cannot post update
            embed = discord.Embed(title=interaction.user.name, color=discord.Colour.red())
            embed.add_field(name=f"",
                            value=f"You have not enrolled for this {self.values[0]} challenge")

            await interaction.response.send_message("", embed=embed)


class UpdateModal(discord.ui.View):
    def __init__(self, server_id, user_id):
        super().__init__()
        self.add_item(ChallengesDropDownForPostingUpdate(server_id=server_id, user_id=user_id))
