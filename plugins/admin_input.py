from main import app
from pyrogram import filters
from database.settings import update_setting
from database.users import get_state, set_state

ADMIN_ID = 123456789  # Replace with your Telegram ID

@app.on_message(filters.private & filters.user(ADMIN_ID) & ~filters.command("settings"))
async def admin_input_handler(client, message):
    user_id = message.from_user.id
    state = await get_state(user_id)

    if not state or "await_input" not in state:
        return  # No pending input

    input_for = state["await_input"]
    text = message.text.strip()

    if input_for == "admin_force_channel":
        # Expecting comma-separated list of usernames or IDs
        channels = [ch.strip() for ch in text.split(",")]
        await update_setting("force_channels", channels)
        await message.reply(f"✅ Force channels updated:\n{channels}")
    elif input_for == "admin_max_results":
        try:
            value = int(text)
            await update_setting("max_results", value)
            await message.reply(f"✅ Max results set to {value}")
        except:
            await message.reply("❌ Please enter a valid number")
    elif input_for == "admin_files_caption":
        await update_setting("files_caption", text)
        await message.reply(f"✅ Files caption updated:\n{text}")
    elif input_for == "admin_set_shortlink":
        await update_setting("shortlink_api", text)
        await update_setting("shortlink_enabled", True)
        await message.reply(f"✅ Shortlink API set and enabled")
    elif input_for == "admin_tutorial_link":
        await update_setting("tutorial_link", text)
        await message.reply(f"✅ Tutorial link updated:\n{text}")
    else:
        await message.reply("❌ Unknown setting")

    # Clear await_input state
    state.pop("await_input")
    await set_state(user_id, state)
