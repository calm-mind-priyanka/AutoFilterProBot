from database.connection import db

SETTINGS_COLLECTION = db["settings"]

DEFAULT_SETTINGS = {
    "force_channels": [],
    "max_results": 10,
    "imdb": True,
    "spell_check": True,
    "auto_delete": 0,
    "files_mode": "document",
    "files_caption": "🎬 Powered by AutoFilterPro",
    "shortlink_enabled": False,
    "shortlink_api": "",
    "result_mode": "button"
}

async def get_settings():
    settings = await SETTINGS_COLLECTION.find_one({"_id": "global"})
    if not settings:
        await SETTINGS_COLLECTION.insert_one({"_id": "global", **DEFAULT_SETTINGS})
        return DEFAULT_SETTINGS
    return settings

async def update_setting(key: str, value):
    await SETTINGS_COLLECTION.update_one(
        {"_id": "global"},
        {"$set": {key: value}},
        upsert=True
    )
