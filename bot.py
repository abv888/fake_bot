import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers.start import router as start_router
from database.storage import async_db

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/bot.log')
    ]
)

logger = logging.getLogger(__name__)

async def on_startup():
    """Startup event handler"""
    try:
        logger.info("🔧 Initializing database connection pool...")
        await async_db.init_pool()
        logger.info("✅ Database pool initialized successfully")
        
        # Test database connection
        health = await async_db.health_check()
        if health:
            logger.info("✅ Database health check passed")
        else:
            logger.warning("⚠️ Database health check failed")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        # Continue without database (graceful degradation)

async def on_shutdown():
    """Shutdown event handler"""
    try:
        logger.info("🔄 Closing database connection pool...")
        await async_db.close_pool()
        logger.info("✅ Database pool closed successfully")
    except Exception as e:
        logger.error(f"❌ Error closing database pool: {e}")

# Initialize bot and dispatcher
async def main():
    # Initialize Bot instance with default properties using the new method (aiogram 3.7.0+)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher with memory storage for FSM
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(start_router)
    
    # Set up startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        # Skip pending updates and start polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🚀 Starting Casino bot polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
    except Exception as e:
        logger.error(f"❌ Error during bot polling: {e}")
        raise
    finally:
        # Ensure cleanup on exit
        await on_shutdown()

if __name__ == "__main__":
    logger.info("🎯 Starting Casino bot with async database support")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Bot stopped by user!")
    except Exception as e:
        logger.error(f"💥 Critical error: {e}")
        sys.exit(1)
