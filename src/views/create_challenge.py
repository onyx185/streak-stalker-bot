import discord
from discord.ext import commands
from discord import ui, Interaction
from typing import List, Any
from discord._types import ClientT
from datetime import datetime
import uuid
from src.data.create_challenge import MODAL_FIELDS
from src.types.create_challenge_types import ChallengeDocType
from src.database.create_challenge import insert_challenge
from src.database.parse_url import parse_hashtags


class ViewChannels(discord.ui.View):
    ctx: commands.context

    def __init__(self, ctx: commands.context):
        super().__init__()
        self.ctx = ctx
        self.add_item(SelectChannels(self.ctx))


class SelectChannels(discord.ui.Select):
    ctx: commands.context

    def __init__(self, ctx: commands.context):
        self.ctx = ctx

        options = [discord.SelectOption(label=channel.name, value=channel.id)
                   for channel in self.ctx.guild.text_channels]

        super().__init__(min_values=1, max_values=1,
                         placeholder='Select a channel to create challenge in.', options=options)

    async def callback(self, interaction: Interaction[ClientT]):
        try:
            selected_option = self.get_selected_option()
            if not selected_option:
                raise Exception()
            modal_title = "Creating Challenge in {0} Channel".format(
                selected_option['label'])
            await interaction.response.send_modal(
                ChallengeModal(self.ctx, selected_option, title=modal_title))
        except Exception as e:
            print(f'{e}')
    
    def get_selected_option(self):
        selected_option = {}
        for option in self.options:
            if str(option.value) == str(self.values[0]):
                selected_option = {
                    'label': option.label, 'value': option.value}
        return selected_option


class ChallengeModal(discord.ui.Modal):
    ctx: commands.context

    def __init__(self, ctx: commands.context, challengeOption, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        super().__init__()
        self.add_rows()
        self.channel_id = challengeOption['value']

    def add_rows(self):
        for field in MODAL_FIELDS:
            self.add_item(discord.ui.TextInput(label=field['label'], placeholder=field['placeholder'],
                                               default=field['default'], required=field['required'],
                                               custom_id=field['key_name']))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            doc: ChallengeDocType = {}

            for field in interaction.data['components']:
                key = str(field['components'][0]['custom_id']).strip()
                value = str(field['components'][0]['value']).strip()
                doc[key] = value

                doc['hashtags'] = parse_hashtags(doc['hashtags'])
                doc['challenge_id'] = str(uuid.uuid4())
                doc['server_id'] = interaction.guild_id
                doc['channel_id'] = self.channel_id
                doc['created_by'] = interaction.user.id
                doc['created_date'] = datetime.utcnow().isoformat() + "Z"
                response = insert_challenge(doc)

                if(response['is_inserted']):
                    embed = discord.Embed(title="Challenge Created", description= "The challenge has been created. Participants can accept and post update messages once the challenge starts.",color=discord.Colour.green())
                    embed.add_field(name="Challenge Name", value=response['doc']['challenge_name'], inline=False)
                    embed.add_field(name="Start Date", value=response['doc']['start_date'], inline=False)
                    embed.add_field(name="End Date", value=response['doc']['end_date'], inline=False)
                    return await interaction.response.send_message('', embed=embed)
                else:
                    return await interaction.response.send_message(response['message'])
        except Exception as e:
            await interaction.response.send_message("Something went wrong, try again.")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(error)
