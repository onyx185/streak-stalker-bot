from typing import TypedDict, Dict, List
from datetime import datetime

ContextInfoType = TypedDict(
    'ContextInfoType', {'server_id': str, 'user_id': int}, total=True)

ChannelOptionType = TypedDict(
    'ChannelOptionType', {'name': str, 'id': int}, total=True)

class ChallengeDocType(TypedDict):
    challenge_id: str
    server_id: int
    channel_id: int
    challenge_name: str
    start_date: str
    end_date: str
    hashtags: List[str]
    platform: str
    created_by: int
    created_date: str
    
class InsertChallengeResponse(TypedDict):
    doc: ChallengeDocType
    is_inserted: bool
    message: str
