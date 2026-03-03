from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.tokens import create_token, validate_token
from database.settings import get_settings

BASE_SHORTLINK_URL = "https://yourdomain.com/download"  # Example

@app.on_callback_query(filters.regex(r"file_"))
async def shortlink_wrapper(client, callback_query):
    user_id = callback_query.from_user.id
    file_id = callback_query.data.split("_")[1]

    settings = await get_settings()
    shortlink_enabled = settings.get("shortlink_enabled", False)

    if shortlink_enabled:
        token = await create_token(user_id, file_id, expires_in=300)  # 5 min expiry
        short_url = f"{BASE_SHORTLINK_URL}?token={token}"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Download Link", url=short_url)]])
        await callback_query.message.edit_text(
            "✅ Your temporary download link is ready!",
            reply_markup=kb
        )
    else:
        # If shortlink OFF, pass to normal delivery
        from plugins.delivery import delivery_handler
        await delivery_handler(client, callback_query)
