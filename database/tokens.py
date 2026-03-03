from database.connection import db
import datetime

TOKENS_COLLECTION = db["tokens"]

async def create_token(user_id: int, file_id: str, expires_in: int = 300):
    token = f"{user_id}_{file_id}_{int(datetime.datetime.utcnow().timestamp())}"
    data = {
        "token": token,
        "user_id": user_id,
        "file_id": file_id,
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    await TOKENS_COLLECTION.insert_one(data)
    return token

async def validate_token(token: str):
    record = await TOKENS_COLLECTION.find_one({"token": token})
    if not record:
        return None
    if datetime.datetime.utcnow() > record["expires_at"]:
        await TOKENS_COLLECTION.delete_one({"token": token})
        return None
    return record
