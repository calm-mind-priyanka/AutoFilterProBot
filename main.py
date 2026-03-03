from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

app = Client(
    "AutoFilterProBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    workers=50
)

# Import plugins to register handlers
from plugins import start, search, filters, delivery, admin_panel, force_sub

if __name__ == "__main__":
    app.run()
