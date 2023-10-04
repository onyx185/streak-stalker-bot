import discord


class DiscordButton(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎")
    async def button_callback(self, interaction, button):
        button.disabled = True
        await interaction.response.send_message("You clicked the button!")