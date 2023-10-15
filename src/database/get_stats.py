from typing import List
from src.database.database import challenges_collection, UsersChallenges_collection, UsersStreak_collection
from src.types.create_challenge_types import ChallengeDocType
from src.utils.dates import get_date
from datetime import date, datetime
import pandas as pd
import seaborn as sns
import io
import base64

def is_same_date(date1: str, date2: str, separator='-') -> bool:
    # date dd-mm-yyy
    date1_parts = date1.split(separator)
    date2_parts = date2.split(separator)
    d1 = date(date1_parts[2], date1_parts[1], date1_parts[0])
    d2 = date(date2_parts[2], date2_parts[1], date2_parts[0])
    return d1 == d2


def get_stats(server_id: str)-> str:
    challenges: List[ChallengeDocType] = list(challenges_collection.find(
        {'server_id': server_id}))
    challenge_ids = [challenge['challenge_id'] for challenge in challenges]
    user_challenges = list(UsersChallenges_collection.find(
        {'$and': [{'challenge_id': {'$in': challenge_ids}}, {'server_id': server_id}]}))
    user_ids = [user_challenge['user_id']
                for user_challenge in user_challenges]
    user_streaks = list(UsersStreak_collection.find(
        {'$and': [{'user_id': {'$in': user_ids}}, {'challenge_id': challenge_ids}]}))
    stats = []
    for challenge in challenges:
        challenge_item={}
        challenge_item['challenge_name'] = challenge['challenge_name']
        challenge_item['total_participants_count'] = len(list(filter(
            lambda item: item['challenge_id'] == challenge['challenge_id'], user_challenges)))
        challenge_item['eligible_users_count'] = len(list(filter(
            lambda item: (item['challenge_id'] == challenge['challenge_id'] and is_same_date(item['last_posted_date'].strftime('%d-%m-%Y'), challenge['end_date'])), user_streaks)))
        challenge_item['ineligible_users_count'] = challenge_item['total_participants_count'] - challenge_item['eligible_users_count']
        stats.append(challenge_item)
    df = pd.DataFrame(stats, columns=["challenge_name", "total_participants_count", "eligible_users_count", "ineligible_users_count"])
    plot = sns.catplot(data=df, x="challenge_name", y="total_participants_count", errorbar=("pi", 95), kind="bar")
    buffer = io.BytesIO()
    # Save the Seaborn plot as an image in the buffer
    plot.savefig(buffer, format="png")
    buffer.seek(0)  # Reset the buffer to the beginning

    # Convert the buffer to a base64 encoded image string
    img_string = base64.b64encode(buffer.read()).decode()
    return img_string
