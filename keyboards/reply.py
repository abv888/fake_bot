from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Main menu keyboard
def get_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="About the Webinar", callback_data="conference_info")
    kb.button(text="About the Speaker", callback_data="speaker_info")
    kb.button(text="Useful Materials", callback_data="materials")
    kb.button(text="Game Facts", callback_data="top_casinos")
    kb.button(text="Top 5 Services", callback_data="trading_services")
    kb.button(text="Responsible Playing", callback_data="responsible_gambling")
    
    # Adjust the layout of the keyboard - 1 button per row
    kb.adjust(1)
    return kb.as_markup()

# Conference registration keyboard
def get_conference_registration_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="I Agree", callback_data="conference_agree")
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    kb.adjust(1)
    return kb.as_markup()

# Conference info keyboard
def get_conference_info_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Register Now", callback_data="register_conference")
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    kb.adjust(1)
    return kb.as_markup()

# After registration keyboard
def get_after_registration_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()

# Materials keyboard
def get_materials_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Game Basics", callback_data="basic_materials")
    kb.button(text="Game Strategies", callback_data="advanced_materials")
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    kb.adjust(1)
    return kb.as_markup()

# Trading services keyboard
def get_trading_services_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()

# Speaker info keyboard
def get_speaker_info_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()

# Top casinos keyboard
def get_top_casinos_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()

# Responsible gambling keyboard
def get_responsible_gambling_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()