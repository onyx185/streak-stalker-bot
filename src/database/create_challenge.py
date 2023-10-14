import re
import time
import datetime
from src.types.create_challenge_types import ChallengeDocType, InsertChallengeResponse
from src.database.database import challenges_collection
from src.constant import *

def get_date(date_str:str, separator: str):
    #dd-mm-yyyy
    date_arr = date_str.split(separator)
    return datetime.date(int(date_arr[2]),int(date_arr[1]), int(date_arr[0]))


def is_date_valid(start_date: str, end_date: str):
    try:
        is_start_date_valid = re.match(VALID_DATE_REGEX, start_date, flags=0)
        is_end_date_valid = re.match(VALID_DATE_REGEX, end_date, flags=0)
        if (is_start_date_valid and is_end_date_valid):
            cur_time = datetime.datetime.now()
            date1 = get_date(start_date,'-')
            date2 = get_date(end_date, '-')
            date_today = get_date(f'{cur_time.day}-{cur_time.month}-{cur_time.year}', '-')
            if (date1 >= date2):
                raise Exception('Start Date must be less than End Date')
            elif (date_today > date1):
                raise Exception("Start Date cannot be before today's date")
        else:
            raise Exception('Please enter date in a specified pattern')
    except Exception as e:
        return {'is_valid': False, 'message': str(e)}

    return {'is_valid': True, 'message': ''}


def insert_challenge(doc: ChallengeDocType) -> InsertChallengeResponse:
    try:
        date_res = is_date_valid(doc['start_date'], doc['end_date'])
        if (not date_res['is_valid']):
            raise Exception(date_res['message'])
        is_doc_present = challenges_collection.count_documents({'challenge_name': {
                                                               '$regex': f"^{doc['challenge_name']}$", '$options': 'i'}, 'server_id': doc['server_id']}, limit=1) != 0
        if is_doc_present:
            raise Exception('Challenge Name is already present.')
        challenges_collection.insert_one(doc)
        return {'is_inserted': True, 'message': 'Successfully created the challenge.', 'doc': doc}
    except Exception as e:
        return {'is_inserted': False, 'message': str(e)}

