from src.database.database import UsersChallenges_collection, challenges_collection
from datetime import datetime, timedelta, timezone
import requests


class UserAlerts:
    def __init__(self):
        self.today = datetime.now(tz=timezone(timedelta(hours=5, minutes=30)))

    def get_not_posted_users_details(self) -> dict:

        query = {'last_posted_date': {
            '$lt': self.today
        }}

        results = UsersChallenges_collection.find(query)

        user_ids_and_challenge_ids = {'user_id': [], 'challenge_id': [], 'challenge_name': []}

        for result in results:
            user_ids_and_challenge_ids['user_id'].append(result['user_id'])
            user_ids_and_challenge_ids['challenge_id'].append(result['challenge_id'])

        challenge_ids = user_ids_and_challenge_ids['challenge_id']
        challenge_names = self._get_challenges_name(challenge_ids=challenge_ids)

        user_ids_and_challenge_ids['challenge_name'] = challenge_names

        return user_ids_and_challenge_ids

    def get_today_posted_members(self):
        query = {'last_posted_date': self.today}

        results = UsersChallenges_collection.find(query)

        if results:
            return len(list(results))
        else:
            return 0

    def _get_challenges_name(self, challenge_ids: list) -> list:

        query = {
            'challenge_id': {
                '$in': challenge_ids
            }
        }
        results = challenges_collection.find(query)
        challenge_names = []

        for result in results:
            challenge_names.append(result['challenge_name'])

        return challenge_names


def get_motivational_quote():
    url = "https://api.quotable.io/random?tags=knowledge|education|change|inspiration|discipline|consistency"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        quote = {'content': data['content'], 'author': data['author']}

        return quote
    else:
        return "Failed to fetch a quote."
