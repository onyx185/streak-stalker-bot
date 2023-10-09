from typing import TypedDict
from datetime import datetime

ContextInfoType = TypedDict(
    'ContextInfoType', {'server_id': str, 'user_id': int}, total=True)

ChannelOptionType = TypedDict(
    'ChannelOptionType', {'name': str, 'id': int}, total=True)

class ChallengeDocType(TypedDict):
    challenge_name : str
    challenge_id: str
    start_date: datetime
    end_date: datetime
    hashtag: str
    platform: str
    created_by: str
    created_date: datetime

