from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.files import search_files
from utils.pagination import build_pagination_buttons

RESULTS_PER_PAGE = 5

async def get_filter_values(files):
    languages = sorted(set(f["language"] for f in files))
    qualities = sorted(set(f["quality"] for f in files))
    seasons = sorted(set(f["season"] for f in files if f["season"] > 0))
    return languages, qualities, seasons

def build_filter_keyboard(languages, qualities, seasons):
    buttons = []

    if languages:
        lang_buttons = [InlineKeyboardButton(l, callback_data=f"lang_{l}") for l in languages]
        buttons.append(lang_buttons)
    if qualities:
        quality_buttons = [InlineKeyboardButton(q, callback_data=f"quality_{q}") for q in qualities]
        buttons.append(quality_buttons)
    if seasons:
        season_buttons = [InlineKeyboardButton(f"S{s}", callback_data=f"season_{s}") for s in seasons]
        buttons.append(season_buttons)

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="filter_back")])
    return InlineKeyboardMarkup(buttons)

@app.on_callback_query(filters.regex(r"filter_"))
async def filter_handler(client, callback_query):
    data = callback_query.data
    state = await callback_query.message.chat.get_state(callback_query.from_user.id)
    selected_filters = state.get("selected_filters", {})

    if data.startswith("lang_"):
        selected_filters["language"] = data.split("_")[1]
    elif data.startswith("quality_"):
        selected_filters["quality"] = data.split("_")[1]
    elif data.startswith("season_"):
        selected_filters["season"] = int(data.split("_")[1])
    elif data == "filter_back":
        selected_filters = {}

    await callback_query.message.chat.set_state(callback_query.from_user.id, {"selected_filters": selected_filters})

    # Fetch files again with filters
    query = state.get("last_query", "")
    filter_dict = {}
    if "language" in selected_filters:
        filter_dict["language"] = selected_filters["language"]
    if "quality" in selected_filters:
        filter_dict["quality"] = selected_filters["quality"]
    if "season" in selected_filters:
        filter_dict["season"] = selected_filters["season"]

    files_cursor = await search_files(query, filter_dict, limit=50)
    files = [f async for f in files_cursor]

    # Dynamic keyboard
    languages, qualities, seasons = await get_filter_values(files)
    keyboard = build_filter_keyboard(languages, qualities, seasons)

    await callback_query.message.edit_reply_markup(keyboard)
