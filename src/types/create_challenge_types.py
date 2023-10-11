from typing import TypedDict
from datetime import datetime

ContextInfoType = TypedDict(
    'ContextInfoType', {'server_id': str, 'user_id': int}, total=True)

ChannelOptionType = TypedDict(
    'ChannelOptionType', {'name': str, 'id': int}, total=True)

class ChallengeDocType(TypedDict):
    challenge_id: str
    server_id: int
    challenge_name : str
    start_date: str
    end_date: str
    hashtag: str
    platform: str
    created_by: int
    created_date: str

