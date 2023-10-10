from src.database.parse_url import parse_hashtags, parse_urls, find_social_media, parse_linkdein_url
from src.database.database import UsersChallenges_collection, UsersStreak_collection
from datetime import datetime, timedelta, timezone
import json

with open("./src/database/dummydata.json", 'r') as file:
    dummy_data = json.loads(file.read())


class ChallengeDetails:
    def __init__(self, server_id: str | int):
        self.server_id = str(server_id)

    def get_challenges(self) -> dict:

        challenges = {}

        for dum in dummy_data:
            if dum['server_id'] == self.server_id:
                challenges[dum['challenge_name']] = dum['challenge_id']

        return challenges

    def get_challenge_dates(self, challenge_id: int | str) -> dict:

        dates = {}

        for dum in dummy_data:
            if dum['challenge_id'] == challenge_id:
                dates['start_date'] = dum['start_date']
                dates['end_date'] = dum['end_date']

        return dates

    def get_eligible_hastags(self, challenge_id: int | str) -> dict:
        hastags = []

        for dum in dummy_data:
            if dum['challenge_id'] == challenge_id:
                hastags = dum['hastags']

        return hastags


class UserChallenges:
    def __init__(self, server_id, user_id):
        self.server_id = server_id
        self.user_id = user_id

    def is_user_enrolled(self, challenge_id: int | str):
        try:
            query = {'challenge_id': int(challenge_id), 'user_id': int(self.user_id)}
            result = UsersChallenges_collection.find_one(query)

            if result:
                return True
            return False
        except:
            return True

    def add_challenge_to_user(self, channel_id: int, challenge_id: int | str):
        data = {}

        data['user_id'] = int(self.user_id)
        data['server_id'] = int(self.server_id)
        data['challenge_id'] = int(challenge_id)
        data['channel_id'] = int(channel_id)
        data['status'] = 'active'
        data['last_posted_date'] = None  # when challenge is added date will be none

        try:
            inserted = UsersChallenges_collection.insert_one(data)
        except Exception as e:
            print(e)

        return True


class UserPostUpdate(UserChallenges):
    def __init__(self, server_id, user_id):
        super().__init__(server_id, user_id)
        self.kick_out = False
        self.already_posted = False

    def eligible_to_post(self, challenge_id):
        try:
            query = {'challenge_id': int(challenge_id), 'user_id': int(self.user_id)}
            projection = {'last_posted_date': 1}

            # check the last_post_date
            result = UsersChallenges_collection.find_one(query, projection)['last_posted_date']

            if result:
                last_posted = result.date()

                present = datetime.now(tz=timezone(timedelta(hours=5, minutes=30))).date()

                difference = int(abs((present - last_posted).days))

                if difference == 1:
                    return True
                elif difference > 1:
                    # lost the streak so kick out
                    self.kick_out = True
                elif difference == 0:
                    # already posted
                    self.already_posted = True

                return False
            else:
                # condition where last post date is none, i.e this is his first post
                return True

        except Exception as e:
            print(e)

    def add_post_update(self, challenge_id, data: dict):

        data['hashtags'] = parse_hashtags(data['hashtags'])

        data['social_media_links'] = parse_urls(data['social_media_links'])

        data['media_content'] = {}

        if data['social_media_links']:
            for link in data['social_media_links']:
                media = find_social_media(link)

                data['media_content'][media] = {}
                data['media_content'][media] = "No Details"

                if media == 'linkedin':
                    media_data = parse_linkdein_url(link)
                    data['media_content']['linkedin'] = media_data

        try:
            # add data to database
            UsersStreak_collection.insert_one(data)

            # to update last post date
            # "where" condition
            filter_condition = {'user_id': int(self.user_id),
                                'challenge_id': int(challenge_id)}


            # update last post date
            update_operation = {
                '$set': {
                    'last_posted_date': data['submited_date']
                }
            }

            UsersChallenges_collection.update_one(filter_condition, update_operation)

        except Exception as e:
            print(e)

        return True

# 1110758349127028737 - user_id