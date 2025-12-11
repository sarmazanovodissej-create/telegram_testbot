from aiogram import Bot, Dispatcher

import asyncio
from config import BOT_TOKEN
from handlers import register_handlers
from scheduler import start_scheduler
from db import init_db


async def main():
    print("Инициализируем базу данных") 
    await init_db()

    start_scheduler()
    print("Фоновые задачи запущены...")
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await register_handlers(dp)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())