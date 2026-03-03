from database.connection import db

USERS_COLLECTION = db["users"]

async def add_user(user_id: int):
    user = await USERS_COLLECTION.find_one({"user_id": user_id})
    if not user:
        await USERS_COLLECTION.insert_one({
            "user_id": user_id,
            "joined_at": None,
            "state": {}
        })

async def get_state(user_id: int):
    user = await USERS_COLLECTION.find_one({"user_id": user_id})
    if user:
        return user.get("state", {})
    return None

async def set_state(user_id: int, state: dict):
    await USERS_COLLECTION.update_one(
        {"user_id": user_id},
        {"$set": {"state": state}},
        upsert=True
    )
