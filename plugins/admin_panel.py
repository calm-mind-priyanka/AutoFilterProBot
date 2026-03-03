from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.settings import get_settings, update_setting

ADMIN_ID = 123456789  # Your Telegram ID

def build_settings_keyboard(settings):
    kb = [
        [InlineKeyboardButton("👥 FORCE CHANNEL", callback_data="admin_force_channel"),
         InlineKeyboardButton("ℹ️ MAX RESULTS", callback_data="admin_max_results")],
        [InlineKeyboardButton("満 IMDB", callback_data="admin_imdb"),
         InlineKeyboardButton("🔍 SPELL CHECK", callback_data="admin_spell_check")],
        [InlineKeyboardButton("🗑️ AUTO DELETE", callback_data="admin_auto_delete"),
         InlineKeyboardButton("📚 RESULT MODE", callback_data="admin_result_mode")],
        [InlineKeyboardButton("🗂 FILES MODE", callback_data="admin_files_mode"),
         InlineKeyboardButton("📝 FILES CAPTION", callback_data="admin_files_caption")],
        [InlineKeyboardButton("🥁 TUTORIAL LINK", callback_data="admin_tutorial_link"),
         InlineKeyboardButton("🧷 SET SHORTLINK", callback_data="admin_set_shortlink")],
        [InlineKeyboardButton("‼️ CLOSE SETTINGS MENU ‼️", callback_data="admin_close_settings")]
    ]
    return InlineKeyboardMarkup(kb)

@app.on_message(filters.private & filters.user(ADMIN_ID) & filters.command("settings"))
async def admin_settings(client, message):
    settings = await get_settings()
    kb = build_settings_keyboard(settings)
    await message.reply_text("⚙️ Admin Settings Panel", reply_markup=kb)

# Callback handler for all admin buttons
@app.on_callback_query(filters.regex(r"admin_"))
async def admin_buttons(client, callback_query):
    data = callback_query.data
    settings = await get_settings()

    # Example toggle logic
    if data == "admin_imdb":
        new_value = not settings.get("imdb", True)
        await update_setting("imdb", new_value)
        await callback_query.answer(f"IMDB toggled to {new_value}")
    elif data == "admin_spell_check":
        new_value = not settings.get("spell_check", True)
        await update_setting("spell_check", new_value)
        await callback_query.answer(f"Spell Check toggled to {new_value}")
    elif data == "admin_auto_delete":
        # Cycle through 0, 30, 60 seconds as example
        current = settings.get("auto_delete", 0)
        new_value = 0 if current >= 60 else current + 30
        await update_setting("auto_delete", new_value)
        await callback_query.answer(f"Auto Delete set to {new_value} sec")
    elif data == "admin_close_settings":
        await callback_query.message.delete()
        await callback_query.answer("⚡ Settings closed")
    else:
        # For buttons needing input, set admin state
        await callback_query.message.chat.set_state(callback_query.from_user.id, {"await_input": data})
        await callback_query.answer("Enter new value in chat")
