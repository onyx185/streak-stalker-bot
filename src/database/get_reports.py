import pandas as pd
from datetime import datetime
from src.database.database import challenges_collection, UsersChallenges_collection
import operator
import numpy as np


class GetReport:
    def __init__(self, ctx, challenge_id):
        self.challenge_id = challenge_id
        self.ctx = ctx
        self.server_id = ctx.guild.id
        self.data_present = self._any_data_present()

    def _any_data_present(self):
        if self.challenge_id == 0:
            users = UsersChallenges_collection.find_one({'server_id': self.server_id}, {'_id': 0})
        else:
            users = UsersChallenges_collection.find_one({'server_id': self.server_id,'challenge_id': self.challenge_id}, {'_id': 0})

        if users:
            return True
        else:
            return False

    def get_report(self):
        df_users = self._get_users_details(challenge_id=self.challenge_id)

        df_users['last_posted_date'] = df_users['last_posted_date'].astype('datetime64[ns]')
        df_users['eligible'] = np.where(
            operator.and_(df_users['last_posted_date'].dt.date == datetime.now().date(),
                          df_users['status'] == 'active'),
            "Yes", "No")

        df_challenges = self._get_challenges_details(challenge_id=self.challenge_id)

        df_final = df_challenges[['challenge_name', 'start_date',
                                  'end_date', 'challenge_id']].merge(df_users, on='challenge_id')

        df_final[['user_id', 'server_id', 'channel_id']] = df_final[['user_id',
                                                                     'server_id', 'channel_id']].astype('str')
        df_final = df_final.rename(columns={
                         'eligible': "Is Eligible",
                        'status': "Challenge Status",
                        'user_id': "User ID",
                        'last_posted_date': "Last Active",
                        'challenge_name': "Challenge Participated",
                        'start_date': "Challenge Start Date",
                        'end_date': "Challenge End Date",
                        'discord_username': 'Discord User Name'
                        })

        col_order = ['User ID', 'Discord User Name', 'Challenge Participated', 'Challenge Start Date',
                     'Challenge End Date', 'Challenge Status', 'Last Active', 'Is Eligible']

        return df_final[col_order]

    def _get_users_details(self, challenge_id):
        if challenge_id == 0:
            users = UsersChallenges_collection.find({'server_id': self.server_id}, {'_id': 0})
        else:
            users = UsersChallenges_collection.find({'server_id': self.server_id, 'challenge_id': challenge_id},
                                                    {'_id': 0})

        users_list = list(users)
        df_users = pd.DataFrame(users_list)

        # will be filled in reports view
        df_users['discord_username'] = "not found"

        return df_users

    def _get_challenges_details(self, challenge_id):

        if challenge_id == 0:
            challenges = challenges_collection.find({'server_id': self.server_id}, {'_id': 0})
        else:
            challenges = challenges_collection.find({'server_id': self.server_id, 'challenge_id': challenge_id},
                                                    {'_id': 0})

        challenges_list = list(challenges)
        df_challenges = pd.DataFrame(challenges_list)

        return df_challenges
