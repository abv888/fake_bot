from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

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
        reply_markup=get_materials_kb()
    )

@router.callback_query(F.data == "basic_materials")
async def process_basic_materials(callback: CallbackQuery):
    """Handle basic materials button callback"""
    await callback.answer()
    
    # Here you would typically send files or links to basic materials
    await callback.message.edit_text(
        text="<b>IOST Basics:</b>\n\n"
             "• What is IOST blockchain and its unique features\n"
             "• Understanding IOST token utility and economics\n"
             "• How to create and secure an IOST wallet\n"
             "• Navigating the IOST ecosystem and applications",
        reply_markup=get_materials_kb()
    )

@router.callback_query(F.data == "advanced_materials")
async def process_advanced_materials(callback: CallbackQuery):
    """Handle advanced materials button callback"""
    await callback.answer()
    
    # Here you would typically send files or links to advanced materials
    await callback.message.edit_text(
        text="<b>Airdrop Strategies:</b>\n\n"
             "• How to qualify for IOST airdrops\n"
             "• Maximizing your airdrop allocation\n"
             "• Setting up notifications for upcoming drops\n"
             "• Security practices during airdrops\n"
             "• Tax considerations for airdrop recipients",
        reply_markup=get_materials_kb()
    )

@router.callback_query(F.data == "strategies_materials")
async def process_strategies_materials(callback: CallbackQuery):
    """Handle strategies materials button callback"""
    await callback.answer()
    
    # Here you would typically send files or links to strategies materials
    await callback.message.edit_text(
        text="<b>Binance Guide:</b>\n\n"
             "• Creating and verifying your Binance account\n"
             "• Setting up airdrop eligibility on Binance\n"
             "• Trading IOST on Binance platform\n"
             "• Using Binance Earn features with IOST\n"
             "• Understanding Binance Launchpad participation",
        reply_markup=get_materials_kb()
    )