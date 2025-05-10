from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from keyboards import get_main_menu
from texts.messages import WELCOME_MESSAGE
from database.storage import DatabaseManager

# Create router instance
router = Router()

# Initialize database manager
db = DatabaseManager()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle the /start command"""
    # Add user to database
    db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    # Send welcome message with main menu keyboard
    await message.answer(
        text=WELCOME_MESSAGE,
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.HTML
    )

@router.callback_query(F.data == "main_menu")
async def process_main_menu(callback: CallbackQuery):
    """Handle main menu button callback"""
    # Answer callback to remove loading status
    await callback.answer()
    
    # Edit message with main menu
    await callback.message.edit_text(
        text=WELCOME_MESSAGE,
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.HTML
    )