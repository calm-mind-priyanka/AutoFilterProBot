from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.settings import get_settings

async def check_force_sub(user_id: int):
    """
    Returns True if user is member of all channels, else False
    """
    settings = await get_settings()
    channels = settings.get("force_channels", [])
    if not channels:
        return True  # No channels set, allow access

    for ch in channels:
        try:
            member = await app.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

async def build_join_buttons():
    settings = await get_settings()
    channels = settings.get("force_channels", [])
    buttons = [[InlineKeyboardButton("🔗 Join Channels", url=f"https://t.me/{ch}")]] if channels else []
    return InlineKeyboardMarkup(buttons)

# Example integration in delivery callback
@app.on_callback_query(filters.regex(r"file_"))
async def force_sub_wrapper(client, callback_query):
    user_id = callback_query.from_user.id
    allowed = await check_force_sub(user_id)
    if not allowed:
        kb = await build_join_buttons()
        return await callback_query.answer(
            "❌ You must join all required channels first!",
            show_alert=True
        )
