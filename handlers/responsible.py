from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards import get_responsible_gambling_kb
from texts.messages import RESPONSIBLE_GAMBLING_MESSAGE

# Create router instance
router = Router()

@router.callback_query(F.data == "responsible_gambling")
async def process_responsible_gambling(callback: CallbackQuery):
    """Handle airdrop guidelines button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Send airdrop guidelines message
    await callback.message.edit_text(
        text=RESPONSIBLE_GAMBLING_MESSAGE,
        reply_markup=get_responsible_gambling_kb()
    )