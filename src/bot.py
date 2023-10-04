import os
from src.client_setup import client
from src.commands import *
from src.events import *


def run_discord_bot():
    token = os.getenv('token')

    client.run(token)
