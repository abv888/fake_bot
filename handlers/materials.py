from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards import get_materials_kb, get_main_menu
from texts.messages import MATERIALS_INFO_MESSAGE

# Create router instance
router = Router()

@router.callback_query(F.data == "materials")
async def process_materials(callback: CallbackQuery):
    """Handle materials button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Send materials info message
    await callback.message.edit_text(
        text=MATERIALS_INFO_MESSAGE,
        reply_markup=get_materials_kb(),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "basic_materials")
async def process_basic_materials(callback: CallbackQuery):
    """Handle basic materials button callback"""
    await callback.answer()
    
    # Here you would typically send files or links to basic materials
    await callback.message.edit_text(
        text="Casino Basics:\n\n"
             "• What are casino games and how they work\n"
             "• Understanding odds and house edge\n"
             "• Different types of casino games\n"
             "• Basic casino etiquette and rules",
        reply_markup=get_materials_kb(),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "advanced_materials")
async def process_advanced_materials(callback: CallbackQuery):
    """Handle advanced materials button callback"""
    await callback.answer()
    
    # Here you would typically send files or links to advanced materials
    await callback.message.edit_text(
        text="Game Strategies:\n\n"
             "• Blackjack basic strategy\n"
             "• Roulette betting systems\n"
             "• Poker fundamentals\n"
             "• Baccarat optimal play\n"
             "• Managing your casino bankroll",
        reply_markup=get_materials_kb(),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "strategies_materials")
async def process_strategies_materials(callback: CallbackQuery):
    """Handle strategies materials button callback"""
    await callback.answer()
    
    # Here you would typically send files or links to strategies materials
    await callback.message.edit_text(
        text="Casino Etiquette:\n\n"
             "• Proper table game behavior\n"
             "• Tipping protocols\n"
             "• Interacting with dealers\n"
             "• Dress codes at different casinos\n"
             "• International casino customs",
        reply_markup=get_materials_kb(),
        parse_mode=ParseMode.HTML
    )