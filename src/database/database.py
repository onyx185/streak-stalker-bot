from pymongo import MongoClient
import os

client: MongoClient = MongoClient(os.getenv('mongo_connection_string'))

mongo_db = client['StreakBot']

UsersChallenges_collection = mongo_db['Users_challenges']
UsersStreak_collection = mongo_db['Users_streak']
challenges_collection = mongo_db['Challenges']
