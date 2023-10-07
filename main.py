from dotenv import load_dotenv
from src.bot import *

load_dotenv()

if __name__ == "__main__":
    token = os.getenv('token')
    client.run(token)
