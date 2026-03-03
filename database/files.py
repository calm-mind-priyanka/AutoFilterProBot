from database.connection import db

FILES_COLLECTION = db["files"]

async def add_file(file_data: dict):
    """
    file_data = {
        'file_id': str,
        'name': str,
        'size': int,
        'language': str,
        'quality': str,
        'season': int,
        'episode': int
    }
    """
    await FILES_COLLECTION.insert_one(file_data)

async def get_file(file_id: str):
    return await FILES_COLLECTION.find_one({"file_id": file_id})

async def search_files(query: str, filters: dict, limit: int = 10, skip: int = 0):
    mongo_filter = {"name": {"$regex": query, "$options": "i"}}
    mongo_filter.update(filters)
    cursor = FILES_COLLECTION.find(mongo_filter).skip(skip).limit(limit)
    return cursor

async def count_files(query: str, filters: dict):
    mongo_filter = {"name": {"$regex": query, "$options": "i"}}
    mongo_filter.update(filters)
    count = await FILES_COLLECTION.count_documents(mongo_filter)
    return count
