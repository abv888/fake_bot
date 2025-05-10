import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers import (
    start_router,
    conference_router,
    registration_router,
    services_router,
    materials_router,
    casinos_router,
    responsible_router
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Initialize bot and dispatcher
async def main():
    # Initialize Bot instance with default properties using the new method (aiogram 3.7.0+)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher with memory storage for FSM
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register all routers
    dp.include_router(start_router)
    dp.include_router(conference_router)
    dp.include_router(registration_router)
    dp.include_router(services_router)
    dp.include_router(materials_router)
    dp.include_router(casinos_router)
    dp.include_router(responsible_router)
    
    # Skip pending updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.info("Starting World Casino Guide bot")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")