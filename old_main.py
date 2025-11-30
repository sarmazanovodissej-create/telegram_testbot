import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters  import Command
from aiogram import F

import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("TG_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик комманды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Здравствуй, тебе удалось запустить бота")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "main":
    asyncio.run(main())