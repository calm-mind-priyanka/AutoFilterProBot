import aiohttp
from config import IMDB_API

async def fetch_imdb_info(title: str):
    if not IMDB_API:
        return None
    url = f"https://imdb-api.com/en/API/SearchMovie/{IMDB_API}/{title}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return {"rating": result.get("imDbRating"), "genre": result.get("description")}
    return None
