from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
import re

from keyboards import get_main_keyboard
from texts.messages import WELCOME_MESSAGE
from database.storage import DatabaseManager

# Create router instance
router = Router()

# Initialize database manager
db = DatabaseManager()

@router.message(CommandStart())
async def cmd_start(message: Message, command):
    """Handle the /start command with traffic source tracking"""
    
    # Extract traffic source from start parameter
    traffic_source = None
    if command.args:
        # Clean the argument to extract traffic source
        traffic_source = command.args.strip()
        # Validate traffic source (only allow alphanumeric and underscores)
        if not re.match(r'^[a-zA-Z0-9_-]+$', traffic_source):
            traffic_source = "unknown"
    
    # Add user to database with traffic source
    success = db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        traffic_source=traffic_source
    )
    
    if success:
        from aiogram.types import FSInputFile
        video_path = "promo.MP4"
        video = FSInputFile(video_path)
        # Send welcome message with mini app button
        await message.answer_video(
            video=video,
            caption=WELCOME_MESSAGE,
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
    else:
        # Fallback message if database fails
        await message.answer(
            text="Welcome! There was a technical issue, but you can still participate in the airdrop!",
            reply_markup=get_main_keyboard()
        )

@router.callback_query(F.data == "webapp_clicked")
async def handle_webapp_callback(callback: CallbackQuery):
    """Handle webapp button clicks for tracking"""
    print("CLICK")
    # Track button click
    db.track_button_click(callback.from_user.id)