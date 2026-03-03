from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def build_pagination_buttons(
    page: int,
    total_pages: int,
    prefix: str,
    row_buttons: int = 2
):
    """
    Build inline keyboard buttons for pagination.

    :param page: Current page index (0-based)
    :param total_pages: Total number of pages
    :param prefix: Callback prefix for buttons
    :param row_buttons: Number of buttons per row
    :return: InlineKeyboardMarkup
    """

    buttons = []

    # Previous button
    if page > 0:
        buttons.append(
            InlineKeyboardButton(
                text="⏮ Prev",
                callback_data=f"{prefix}_{page-1}"
            )
        )

    # Current page info
    buttons.append(
        InlineKeyboardButton(
            text=f"Page {page+1}/{total_pages}",
            callback_data="ignore"
        )
    )

    # Next button
    if page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton(
                text="Next ⏭",
                callback_data=f"{prefix}_{page+1}"
            )
        )

    # Arrange buttons in rows
    keyboard = []
    for i in range(0, len(buttons), row_buttons):
        keyboard.append(buttons[i:i+row_buttons])

    return InlineKeyboardMarkup(keyboard)
