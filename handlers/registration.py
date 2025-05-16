from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards import get_speaker_info_kb
from texts.messages import SPEAKER_INFO_MESSAGE

# Create router instance
router = Router()

@router.callback_query(F.data == "speaker_info")
async def process_speaker_info(callback: CallbackQuery):
    """Handle expert info button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Send expert info message
    await callback.message.edit_text(
        text=SPEAKER_INFO_MESSAGE,
        reply_markup=get_speaker_info_kb()
    )
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards import get_speaker_info_kb
from texts.messages import SPEAKER_INFO_MESSAGE

# Create router instance
router = Router()

@router.callback_query(F.data == "speaker_info")
async def process_speaker_info(callback: CallbackQuery):
    """Handle speaker info button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Send speaker info message
    await callback.message.edit_text(
        text=SPEAKER_INFO_MESSAGE,
        reply_markup=get_speaker_info_kb()
    )