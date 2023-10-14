import pandas as pd
from datetime import datetime
from src.database.database import challenges_collection, UsersChallenges_collection
import operator
import numpy as np

class GetReport:
    def __init__(self, server_id):
        self.server_id = server_id
        self.data_present = self._any_data_present()

    def _any_data_present(self):
        users = UsersChallenges_collection.find_one({'server_id': self.server_id}, {'_id': 0})
        if users:
            return True
        else:
            return False

    def get_all_report(self):
        df_users = self._get_users_details()

        df_users['last_posted_date'] = df_users['last_posted_date'].astype('datetime64[ns]')
        df_users['eligible'] = np.where(
            operator.and_(df_users['last_posted_date'].dt.date == datetime.now().date(), df_users['status'] == 'active'),
            "Yes", "No")

        df_challenges = self._get_challengs_details()

        df_final = df_challenges[['challenge_name', 'start_date',
                                  'end_date', 'challenge_id']].merge(df_users, on='challenge_id')

        return df_final


    def _get_users_details(self):
        users = UsersChallenges_collection.find({'server_id': self.server_id}, {'_id': 0})
        users_list = list(users)
        df_users = pd.DataFrame(users_list)

        return df_users

    def _get_challengs_details(self):
        challenges = challenges_collection.find({'server_id': self.server_id}, {'_id': 0})
        challenges_list = list(challenges)
        df_challenges = pd.DataFrame(challenges_list)

        return  df_challenges
