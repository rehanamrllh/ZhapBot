from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Mengembalikan keyboard inline utama untuk bot."""
    keyboard = [
        [
            InlineKeyboardButton(text="🧹 Hapus Memori", callback_data="clear_memory"),
            InlineKeyboardButton(text="📚 Bantuan", callback_data="help_menu")
        ],
        [
            InlineKeyboardButton(text="✨ Ringkas Percakapan", callback_data="summarize_chat")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
