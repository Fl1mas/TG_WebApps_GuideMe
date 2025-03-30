import os
import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import setup  # Импортируем функцию setup из файла handlers.py

# Применяем nest_asyncio, если необходимо
nest_asyncio.apply()

# Загружаем переменные окружения
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера
dp = Dispatcher()

async def main() -> None:
    setup(dp)  # Настраиваем обработчики
    print("Бот запущен!")
    await dp.start_polling(bot)  # Запускаем опрос

if __name__ == '__main__':
    asyncio.run(main())