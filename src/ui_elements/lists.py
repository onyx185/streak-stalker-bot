import discord


class DiscordLists(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose a Flavor!",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, interaction, select):  # the function called when the user is done selecting options

        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

        self.stop()
