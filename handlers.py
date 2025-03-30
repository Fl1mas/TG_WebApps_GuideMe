from aiogram import Dispatcher, types
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command  # Импортируем фильтр Command

def setup(dp: Dispatcher):
    @dp.message(Command("start"))  # Используем фильтр Command
    async def cmd_start(message: types.Message):
        # Создаем кнопки
        button = KeyboardButton(text='ОТКРЫВАЙСЯ', web_app=WebAppInfo(url='https://fl1mas.github.io/TG_WebApps_GuideMe/templates/index.html'))
        
        # Создаем разметку клавиатуры с указанием кнопок
        markup = ReplyKeyboardMarkup(
            keyboard=[[button]],  # Указываем кнопки в виде списка списков
            resize_keyboard=True
        )
        
        await message.answer('Привет! Я ваш бот!', reply_markup=markup)