import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TELEGRAM_BOT_TOKEN
from database import init_db
from handlers import commands, messages, files

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    # Inisialisasi Database
    await init_db()
    
    # Inisialisasi Bot dengan Default Properties
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Inisialisasi Dispatcher
    dp = Dispatcher()

    # Daftarkan router (handlers)
    dp.include_router(commands.router)
    dp.include_router(files.router)
    dp.include_router(messages.router)

    logging.info("Bot mulai berjalan (Long Polling)...")
    
    # Mulai polling (akan memblokir event loop dan terus mendengarkan pesan)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot dihentikan oleh pengguna.")
    except Exception as e:
        logging.error(f"Terjadi kesalahan: {e}")
