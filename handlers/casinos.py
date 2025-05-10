from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards import get_top_casinos_kb
from texts.messages import TOP_CASINOS_MESSAGE

# Create router instance
router = Router()

@router.callback_query(F.data == "top_casinos")
async def process_top_casinos(callback: CallbackQuery):
    """Handle top casinos button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Send top casinos message
    await callback.message.edit_text(
        text=TOP_CASINOS_MESSAGE,
        reply_markup=get_top_casinos_kb(),
        parse_mode=ParseMode.HTML
    )