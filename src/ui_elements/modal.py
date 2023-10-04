import discord

# Define the Questionnaire class
class Questionnaire(discord.ui.Modal, title='Questionnaire Response'):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    # async def on_submit(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
