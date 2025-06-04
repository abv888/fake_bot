from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Main menu keyboard
def get_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="About the HUMA Webinar", callback_data="conference_info")
    kb.button(text="About the DeFi Expert", callback_data="speaker_info")
    kb.button(text="Educational Materials", callback_data="materials")
    kb.button(text="HUMA Finance Info", callback_data="top_casinos")
    kb.button(text="DeFi Tools", callback_data="trading_services")
    
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
    
    kb.button(text="HUMA Finance Basics", callback_data="basic_materials")
    kb.button(text="DeFi Airdrop Strategies", callback_data="advanced_materials")
    kb.button(text="DeFi Guide", callback_data="strategies_materials")
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

# HUMA Finance info keyboard
def get_top_casinos_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()

# Airdrop guidelines keyboard
def get_responsible_gambling_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Back to Menu", callback_data="main_menu")
    
    return kb.as_markup()