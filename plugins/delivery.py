from main import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.files import get_file
from database.settings import get_settings
import asyncio

@app.on_callback_query(filters.regex(r"file_"))
async def delivery_handler(client, callback_query):
    file_id = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id

    # Fetch file from DB
    file_record = await get_file(file_id)
    if not file_record:
        return await callback_query.answer("❌ File not found.", show_alert=True)

    settings = await get_settings()

    # Prepare caption
    caption = settings.get("files_caption", "🎬 Powered by AutoFilterPro")
    mode = settings.get("files_mode", "document")

    try:
        # Notify user in group
        await callback_query.answer("✅ Check your PM, file sent there!")

        # Send file to user privately
        if mode.lower() == "document":
            sent_msg = await client.send_document(
                chat_id=user_id,
                document=file_id,
                caption=caption
            )
        else:
            sent_msg = await client.send_video(
                chat_id=user_id,
                video=file_id,
                caption=caption
            )

        # Auto delete if enabled
        auto_delete_sec = settings.get("auto_delete", 0)
        if auto_delete_sec > 0:
            await asyncio.sleep(auto_delete_sec)
            await sent_msg.delete()

    except Exception as e:
        await callback_query.answer(f"❌ Failed to send: {str(e)}", show_alert=True)
