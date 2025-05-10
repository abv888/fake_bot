from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards import get_trading_services_kb
from texts.messages import CASINO_SERVICES_MESSAGE

# Create router instance
router = Router()

@router.callback_query(F.data == "trading_services")
async def process_trading_services(callback: CallbackQuery):
    """Handle casino services button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Send casino services message
    await callback.message.edit_text(
        text=CASINO_SERVICES_MESSAGE,
        reply_markup=get_trading_services_kb(),
        parse_mode=ParseMode.HTML
    )