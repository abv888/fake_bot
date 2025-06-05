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
       text="<b>BingX Platform Guide:</b>\n\n"
            "• Creating and verifying your BingX trading account\n"
            "• Understanding BingX trading features and tools\n"
            "• How to navigate BingX interface and security settings\n"
            "• BingX copy trading and grid bot strategies",
       reply_markup=get_materials_kb()
   )

@router.callback_query(F.data == "advanced_materials")
async def process_advanced_materials(callback: CallbackQuery):
   """Handle advanced materials button callback"""
   await callback.answer()
   
   # Here you would typically send files or links to advanced materials
   await callback.message.edit_text(
       text="<b>Collaboration Strategies:</b>\n\n"
            "• How to benefit from BingX x HUMA partnership\n"
            "• Maximizing rewards through collaboration features\n"
            "• Trading HUMA tokens on BingX platform\n"
            "• Using integrated DeFi services and yield opportunities\n"
            "• Risk management in collaborative trading",
       reply_markup=get_materials_kb()
   )

@router.callback_query(F.data == "strategies_materials")
async def process_strategies_materials(callback: CallbackQuery):
   """Handle strategies materials button callback"""
   await callback.answer()
   
   # Here you would typically send files or links to strategies materials
   await callback.message.edit_text(
       text="<b>HUMA on BingX:</b>\n\n"
            "• Accessing HUMA Finance services through BingX\n"
            "• Understanding PayFi features and benefits\n"
            "• Income-based lending opportunities on the platform\n"
            "• Cross-platform yield farming and staking options\n"
            "• Advanced trading tools for HUMA ecosystem",
       reply_markup=get_materials_kb()
   )