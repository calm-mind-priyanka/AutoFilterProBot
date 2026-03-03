from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.files import search_files, count_files
from rapidfuzz import fuzz, process
from utils.imdb import fetch_imdb_info
from utils.spell import correct_spelling

RESULTS_PER_PAGE = 5

def build_result_buttons(files, page=0):
    buttons = []
    start = page * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    for f in files[start:end]:
        btn_text = f"{f['name']} [{f['language']} | {f['quality']}]"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=f"file_{f['file_id']}")])
    # Pagination
    if len(files) > end:
        buttons.append([InlineKeyboardButton("➡️ Next Page", callback_data=f"page_{page+1}")])
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.private & filters.text)
async def search_handler(client, message):
    user_input = message.text.strip()
    query = correct_spelling(user_input)

    # Optional filters: empty dict for now
    filters_dict = {}

    total_files = await count_files(query, filters_dict)
    files_cursor = await search_files(query, filters_dict, limit=50)
    files = [f async for f in files_cursor]

    if not files:
        return await message.reply_text("❌ No results found.")

    # Fetch IMDb info for first result
    imdb_info = await fetch_imdb_info(files[0]["name"])

    text = f"🎬 <b>{files[0]['name']}</b>\n"
    if imdb_info:
        text += f"⭐ Rating: {imdb_info.get('rating','N/A')}\n"
        text += f"📅 Genre: {imdb_info.get('genre','N/A')}\n"

    await message.reply_text(
        text,
        reply_markup=build_result_buttons(files, page=0),
        parse_mode="html"
    )
