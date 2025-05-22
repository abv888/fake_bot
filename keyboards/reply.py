from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import MINI_APP_URL

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Get main keyboard with mini app button"""
    kb = InlineKeyboardBuilder()
    
    kb.button(
        text="300% BONUS 🚀",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    return kb.as_markup()