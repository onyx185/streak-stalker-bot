from src.types.create_challenge_types import ChallengeDocType
from src.database.database import challenges_collection

def insert_challenge(doc: ChallengeDocType):
    res = challenges_collection.insert_one(doc)
    return res