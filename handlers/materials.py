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
    text="<b>HUMA Basics:</b>\n\n"
      "• What is HUMA and PayFi technology\n"
      "• Understanding HUMA token utility and economics\n"
      "• How to create and secure a DeFi wallet\n"
      "• Navigating the HUMA ecosystem and applications",
    reply_markup=get_materials_kb()
  )

@router.callback_query(F.data == "advanced_materials")
async def process_advanced_materials(callback: CallbackQuery):
  """Handle advanced materials button callback"""
  await callback.answer()
  
  # Here you would typically send files or links to advanced materials
  await callback.message.edit_text(
    text="<b>DeFi Strategies:</b>\n\n"
      "• How to participate in HUMA ecosystem\n"
      "• Maximizing your rewards through staking\n"
      "• Setting up notifications for protocol updates\n"
      "• Security practices in DeFi participation\n"
      "• Understanding income-based lending mechanics",
    reply_markup=get_materials_kb()
  )

@router.callback_query(F.data == "strategies_materials")
async def process_strategies_materials(callback: CallbackQuery):
  """Handle strategies materials button callback"""
  await callback.answer()
  
  # Here you would typically send files or links to strategies materials
  await callback.message.edit_text(
    text="<b>HUMA Protocol Guide:</b>\n\n"
      "• Getting started with HUMA platform\n"
      "• Understanding PayFi and income-based financing\n"
      "• Using HUMA lending and borrowing features\n"
      "• Governance participation with HUMA tokens\n"
      "• Advanced DeFi strategies and yield optimization",
    reply_markup=get_materials_kb()
  )