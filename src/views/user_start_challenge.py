from typing import Any

import discord
from discord import Interaction
from discord._types import ClientT

from src.database.user_data import ChallengeDetails, UserChallenges


class ChallengesDropDown(discord.ui.Select):
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

        super().__init__(placeholder="Choose the challenge to participate", options=options)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:

        UserChallenge_check = UserChallenges(
                                    server_id=self.server_id,
                                    user_id=self.user_id
                                    )

        # accessing challenge_id using challenge name
        challenge_id = self.challenges_from_db[self.values[0]]['challenge_id']
        channel_id = self.challenges_from_db[self.values[0]]['channel_id']

        already_joined = UserChallenge_check.is_user_enrolled_and_active(challenge_id=challenge_id)


        if already_joined['enrolled']:
            # if already joined user cannot join again
            embed = discord.Embed(title=interaction.user.name, color=discord.Colour.red())
            embed.add_field(name=f"",
                            value=f"You have already enrolled for the {self.values[0]}")

            await interaction.response.send_message("", embed=embed)
        else:
            if int(channel_id) == int(interaction.channel_id):
                data = {}

                data['Username'] = interaction.user.name
                data['ChallengeChoosen'] = self.values[0]

                UserChallenge_check.add_challenge_to_user(
                    challenge_id=challenge_id,
                    channel_id=int(interaction.channel_id)
                )

                required_hashtags = self.challenge_details.get_eligible_hastags(challenge_id=challenge_id)

                rules = ["Post an updated on the challenge on daily basis using **$PostUpdate** command",
                         f"Use {' '.join(required_hashtags)} while posting update",
                         "Maintain Streak to complete the Challenge"]

                embed = discord.Embed(title=data['Username'], color=discord.Colour.green())

                embed.add_field(name="",
                                value=f"You have now started the {data['ChallengeChoosen']}   🎉",
                                inline=True)

                embed.add_field(name="  ", value="   ", inline=False)

                embed.add_field(name="Rules", value="", inline=False)

                for ind, msg in enumerate(rules):
                    embed.add_field(name='', value='✅ ' + msg, inline=False)

                await interaction.response.send_message("", embed=embed)
            else:

                channel_name = self.ctx.guild.get_channel(channel_id)

                embed = discord.Embed(title="Wrong Channel", color=discord.Colour.red())

                embed.add_field(name="",
                                value=f"You are not allowed to start challenge in this channel, please create challenge "
                                      f"in #{channel_name} channel",
                                inline=True)

                await interaction.response.send_message("", embed=embed)


class ChallengesList(discord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.add_item(ChallengesDropDown(ctx))

