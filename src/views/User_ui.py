import discord
from datetime import datetime
from src.database.user_data import add_update_to_database

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

class ChallengesList(discord.ui.View):

    challenges_list_from_db = ["30 Days of Coding Challenge", "Open Quest Challenge"]

    @discord.ui.select(
        placeholder="Choose the challenge to participate",
        options=[discord.SelectOption(label=challenge) for challenge in challenges_list_from_db]
    )

    async def challenge_selected(self, interaction, select_item: discord.ui.Select):
        data={}
        data['Username'] = interaction.user.name
        data['ChallengeChoosen'] = select_item.values[0]

        #get challenges info from database
        #check if user has already opted for the challenge, if yes send message you have clready opted for the challenge
        #if not add challenge name top this user

        already_opted = True
        new_user = False

        if already_opted:
            embed = discord.Embed(title=data['Username'], color=discord.Colour.red())
            embed.add_field(name=f"",
                            value=f"You have already enrolled for the {data['ChallengeChoosen']}")

            await interaction.response.send_message("", embed=embed)

        if new_user:
            rules = ["Post an updated on the challenge on daily basis using **$PostUpdate** command",
                     "Maintain Streak to complete the Challenge"]

            embed = discord.Embed(title=data['Username'], color=discord.Colour.green())

            embed.add_field(name="",
                            value=f"You have now started the {data['ChallengeChoosen']}   🎉",
                            inline=True)

            embed.add_field(name="  ", value="   ",inline=False)

            embed.add_field(name="Rules", value="", inline=False)

            for ind, msg in enumerate(rules):
                embed.add_field(name='', value='✅ '+msg, inline=False)

            await interaction.response.send_message("", embed=embed)



class PostUpdateModal(discord.ui.Modal):
    def __init__(self,username, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        username = username

        self.all_fields = ["User Name", "Date", "Hashtags", "Social Media Links", "Message"]

        self.add_item(discord.ui.TextInput(label=self.all_fields[0], placeholder="Discord Username",
                                           default=username, required=True))
        self.add_item(discord.ui.TextInput(label=self.all_fields[1], placeholder="Post Date",
                                           default=datetime.now().strftime("%Y-%m-%d"),required=True))
        self.add_item(discord.ui.TextInput(label=self.all_fields[2], placeholder="Enter eligible hastags",
                                           required=False))
        self.add_item(discord.ui.TextInput(label=self.all_fields[3], placeholder="Social Media Links",
                                           required=False))
        self.add_item(discord.ui.TextInput(label=self.all_fields[4], style=discord.TextStyle.long,
                                           required=False,
                                           placeholder="Your message"))

    async def on_submit(self, interaction):
        data = {}
        data['Discord_user'] = interaction.user.name
        data['Discord_user_id'] = interaction.user.id
        data['Submitted_in_channel'] = interaction.channel.name

        for ind, field in enumerate(self.all_fields):
            data[field.replace(" ", "_")] = interaction.data['components'][ind]['components'][0]['value']

        #add record to database
        add_update_to_database(data)


        embed = discord.Embed(
            title="Daily Updates",
            color=discord.Colour.green(),  # Pycord provides a class with default colors you can choose from
        )

        embed.add_field(name=f"{data['Discord_user']}",
                        value="Thank you for posting a update")


        await interaction.response.send_message("", embed=embed)

    async def on_error(self, interaction, error: Exception, /) -> None:
        print(error)



class UpdateModal(discord.ui.View):
    @discord.ui.button(label="Post Update", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        await interaction.response.send_modal(PostUpdateModal(username=interaction.user.name, title="Daily Updates"))
