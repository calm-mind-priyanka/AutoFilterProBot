import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

MONGO_URI = os.getenv("MONGO_URI")
MOVIE_CHANNEL = int(os.getenv("MOVIE_CHANNEL"))  # e.g. -1001234567890

IMDB_API = os.getenv("IMDB_API")  # Optional

DEFAULT_FILES_MODE = os.getenv("DEFAULT_FILES_MODE", "document")
