from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputFile
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
    
    # Текст сообщения с форматированием HTML
    promo_text = (
        "🤑 <b>Get 1000x times your stake</b> 🤑\n\n"
        "🔥 If you haven't tried your hand at <b>Lucky Jet</b>, 1win's most adrenaline-pumping crash game, "
        "<b>now is the time!</b> Today you can win <b>x1,000</b>\n\n"
        "Don't miss out - <b>hit the jackpot now!</b> 💸\n\n"
        "Use Promo <b>LUUCKY777</b> and get your <b>300% bonus</b> for your first deposit."
    )
    
    # Создаем клавиатуру с кнопкой для открытия мини-приложения
    web_app_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="300% BONUS 🚀", 
                    web_app=WebAppInfo(url="https://yekazik.com/game1/")
                )
            ]
        ]
    )
    
    # Отправляем видео с текстом и клавиатурой
    try:
        # В aiogram 3.x используем FSInputFile вместо InputFile
        from aiogram.types import FSInputFile
        
        video_path = "promo.MP4"
        video = FSInputFile(video_path)
        
        await message.answer_video(
            video=video,
            caption=promo_text,
            reply_markup=web_app_keyboard,
            parse_mode=ParseMode.HTML
        )
    except FileNotFoundError:
        # Если файл видео не найден, отправляем только текст с кнопкой
        await message.answer(
            text=f"⚠️ Video file not found.\n\n{promo_text}",
            reply_markup=web_app_keyboard,
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