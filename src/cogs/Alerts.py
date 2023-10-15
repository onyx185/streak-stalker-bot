from discord.ext import commands, tasks
import discord
from src.database.user_alerts import UserAlerts, get_motivational_quote
from datetime import datetime, timedelta, timezone
from src.constant import REMINDER_TIME_FOR_ALERT_IN_24H_FORMAT


class Alerts(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_user_last_post_and_send_alert.start()

    def cog_unload(self) -> None:
        self.check_user_last_post_and_send_alert.stop()

    @tasks.loop(hours=5)
    async def check_user_last_post_and_send_alert(self):
        current_time = datetime.now(tz=timezone(timedelta(hours=5, minutes=30))).strftime('%H')

        if current_time in REMINDER_TIME_FOR_ALERT_IN_24H_FORMAT:
        # if True:
            user_alert = UserAlerts()
            user_details = user_alert.get_not_posted_users_details()

            #members already posted
            already_posted = user_alert.get_today_posted_members()

            for user_id, challenge_name in zip(user_details['user_id'], user_details['challenge_name']):
                try:
                    user = await self.client.fetch_user(user_id)

                    print("Posted message")

                    quote = get_motivational_quote()

                    std_color = discord.Colour.red()

                    embed_quotes = discord.Embed(
                        title=f"{quote['content']}",
                        color=std_color
                    )

                    embed_quotes.set_author(name=f"{quote['author']}")

                    embed_message = discord.Embed(
                        title=f"Challenge update remainder 🕔",
                        color=std_color
                    )

                    embed_message.add_field(
                        name=f"{user.display_name}",
                        value=f"\nYou have not posted an update for **{challenge_name}** for the day.👨‍💻\n"
                              f"Please update to maintain the streak 🏆",
                        inline=False
                    )

                    if already_posted == 0:
                        embed_message.add_field(
                            name=f"",
                            value=f"Be the first one to post an update, hurry up!! 🏃‍♂️",
                            inline=False
                        )
                    else:
                        embed_message.add_field(
                            name=f"",
                            value=f"{already_posted} have already posted an update, hurry up!! 🏃‍♂️",
                            inline=False
                        )

                    await user.send("", embeds=[embed_quotes, embed_message])

                except Exception as e:
                    print(e)

async def setup(client):
    await client.add_cog(Alerts(client))
