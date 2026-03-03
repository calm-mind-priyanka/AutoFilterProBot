from main import app
from pyrogram import filters
from database.files import add_file
import re

# Example regex to parse movie info from filename
FILENAME_PATTERN = re.compile(
    r"(?P<name>.+?)\s*\[?(?P<language>Hindi|English|Tamil|Telugu|Malayalam|Kannada|Bengali)?\]?\s*(?P<quality>480p|720p|1080p|4K)?\s*(S(?P<season>\d+))?\s*(E(?P<episode>\d+))?",
    re.IGNORECASE
)

@app.on_message(filters.channel & filters.document)
async def auto_index(client, message):
    filename = message.document.file_name
    file_id = message.document.file_id
    size = message.document.file_size

    match = FILENAME_PATTERN.search(filename)
    if match:
        name = match.group("name").strip()
        language = match.group("language") or "Unknown"
        quality = match.group("quality") or "Unknown"
        season = int(match.group("season") or 0)
        episode = int(match.group("episode") or 0)
    else:
        name = filename
        language = "Unknown"
        quality = "Unknown"
        season = 0
        episode = 0

    file_data = {
        "file_id": file_id,
        "name": name,
        "size": size,
        "language": language,
        "quality": quality,
        "season": season,
        "episode": episode
    }

    await add_file(file_data)
    print(f"Indexed: {name} | {language} | {quality} | S{season}E{episode}")
