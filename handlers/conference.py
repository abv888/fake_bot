from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards import (
    get_conference_info_kb,
    get_conference_registration_kb,
    get_after_registration_kb
)
from texts.messages import (
    CONFERENCE_INFO_MESSAGE,
    CONFERENCE_REQUEST_MESSAGE,
    REGISTRATION_CONFIRMATION_MESSAGE
)
from database.storage import DatabaseManager

# Create router instance
router = Router()

# Initialize database manager
db = DatabaseManager()

@router.callback_query(F.data == "conference_info")
async def process_conference_info(callback: CallbackQuery):
    """Handle webinar info button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Edit message with webinar info
    await callback.message.edit_text(
        text=CONFERENCE_INFO_MESSAGE,
        reply_markup=get_conference_info_kb()
    )

@router.callback_query(F.data == "register_conference")
async def process_register_conference(callback: CallbackQuery):
    """Handle webinar registration button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Check if already registered
    if db.is_registered_for_conference(callback.from_user.id):
        await callback.message.edit_text(
            text="You are already registered for the $HUMA webinar!",
            reply_markup=get_after_registration_kb()
        )
        return
    
    # Show registration confirmation request
    await callback.message.edit_text(
        text=CONFERENCE_REQUEST_MESSAGE,
        reply_markup=get_conference_registration_kb()
    )

@router.callback_query(F.data == "conference_agree")
async def process_conference_agree(callback: CallbackQuery):
    """Handle webinar agreement button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Register user for webinar
    db.register_for_conference(callback.from_user.id)
    
    # Send confirmation message
    await callback.message.edit_text(
        text=REGISTRATION_CONFIRMATION_MESSAGE,
        reply_markup=get_after_registration_kb()
    )