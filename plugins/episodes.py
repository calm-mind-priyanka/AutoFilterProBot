from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.files import search_files

@app.on_callback_query(filters.regex(r"season_\d+"))
async def episodes_handler(client, callback_query):
    season = int(callback_query.data.split("_")[1])
    state = await callback_query.message.chat.get_state(callback_query.from_user.id)
    query = state.get("last_query", "")
    filter_dict = state.get("selected_filters", {})
    filter_dict["season"] = season

    files_cursor = await search_files(query, filter_dict, limit=50)
    files = [f async for f in files_cursor]

    # Build episode buttons
    episodes = sorted(set(f["episode"] for f in files if f["episode"] > 0))
    buttons = []
    for ep in episodes:
        buttons.append([InlineKeyboardButton(f"E{ep}", callback_data=f"episode_{ep}")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="filter_back")])

    keyboard = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_reply_markup(keyboard)
