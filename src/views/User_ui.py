import discord


class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    async def on_timeout(self):
        print("Done")


    @discord.ui.button(label="Start", row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, interaction, button):
        button.disabled = discord.Button.disabled
        button.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(view=self)
        await interaction.channel.send("okay")

    @discord.ui.button(label="Edit", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, interaction, button):
        button.disabled = discord.Button.disabled
        button.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(view=self)
        await interaction.channel.send("okay")


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.all_fields = ["Short Input", "Long Input"]
        self.add_item(discord.ui.TextInput(label=self.all_fields[0]))
        self.add_item(discord.ui.TextInput(label=self.all_fields[1], style=discord.TextStyle.long))


    async def on_submit(self, interaction):
        data = {}
        data['Submitted_by'] = interaction.user.name
        data['Submitted_in_channel'] = interaction.channel.name
        data['Submitted_at'] = interaction.created_at

        for ind, field in enumerate(self.all_fields):
            data[field] = interaction.data['components'][ind]['components'][0]['value']

        print(data)

        embed = discord.Embed(
            title="Get Starated",
            description="Embeds are super easy, barely an inconvenience.",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )

        embed.add_field(name=f"{data['Submitted_by']}",
                        value="")

        embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)

        await interaction.response.send_message("", embed=embed)

    async def on_error(self, interaction, error: Exception, /) -> None:
        print(error)



class ModalView(discord.ui.View):
    @discord.ui.button(label="Send Modal", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        await interaction.response.send_modal(MyModal(title="Modal via Button"))


class MySelect(discord.ui.View):
    answer1 = None
    answer2 = None

    @discord.ui.select(
        placeholder="Choose the age",
        options=[
            discord.SelectOption(label="95"),
            discord.SelectOption(label="105"),
        ]
    )
    async def find_age(self, interaction, select_item: discord.ui.Select):
        print(select_item.values)
        await interaction.response.send_message("Thanks")

