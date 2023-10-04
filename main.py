from src import bot
from dotenv import load_dotenv

# reads .env file and adds to system env variables
load_dotenv()

if __name__ == '__main__':
    bot.run_discord_bot()
