from src.client_setup import client
import discord
from discord.ext import commands
from src.ui_elements import buttons, lists, modal


@client.command()
async def testbutton(ctx):
    await ctx.send("This is a button!", view=buttons.DiscordButton())


@client.command()
async def testlist(ctx):
    await ctx.send("Choose a flavor!", view=lists.DiscordLists())


@client.command(name="modal")
async def testmodal(ctx, interaction: discord.InteractionResponse):
    # print(arg)
    # Create an instance of the Questionnaire and start it
    await interaction.send_modal(modal.Questionnaire())


@client.command(name="start_challenge", description="When this command is invoked, the challenge streak is recorded")
async def start_challenge_command(ctx, *arg):
    full_message = ctx.message.content
    args_passed = arg

    embed = discord.Embed(
        title="My 30days Challenge",
        description="Welcome to the challenge.",
        color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Rules",
                    value="Maintain **30 days** streak to win the challenge")

    embed.set_author(name=ctx.author.display_name,
                     icon_url="https://media.licdn.com/dms/image/C5612AQGpYu4K-fBhNQ/article-cover_image"
                              "-shrink_600_2000/0/1587011267304?e=2147483647&v=beta&t=6FjaWHFAG8qnR9FYRO"
                              "-e9LmJ8Q4OQqYw06ndko5piJM")
    embed.set_thumbnail(url="https://img.freepik.com/free-vector/illustration-business-concept_53876-37559.jpg")
    embed.set_image(url="https://img.freepik.com/free-vector/illustration-business-concept_53876-37559.jpg")

    embed.set_footer(text="Footer! Not yet")  # footers can have icons too

    await ctx.send("", embed=embed)  # Send the embed with some text
