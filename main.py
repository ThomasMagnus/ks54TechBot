import random

from typing import List
from config import admin_id

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from states import States

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from config import TOKEN
from userApp import UserApp

storage = MemoryStorage()
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=storage)

type_app_list: List[str] = ['Администрация', 'Преподаватель', 'Иной сотрудник']


def make_keyboard(items: List[str]) -> ReplyKeyboardMarkup:
    info_btn: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(item) for item in items]
    for item in buttons:
        info_btn.add(item)
    return info_btn


def generate_app_num() -> str:
    app_num: str = ""
    for x in range(6):
        app_num += str(random.randint(0, 10))
    return app_num


start_button: KeyboardButton = KeyboardButton("Составить заявку!")
start_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)

user_app: UserApp = None


@dp.message_handler(commands=['start'], state=None)
async def process_start_message(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await message.answer("Ждём заявок!")
    else:
        await message.answer(
            "Привет! Я твой помощник по составлению заявки на неисправность оборудования!", reply_markup=start_btn)


@dp.message_handler(Text(equals="Составить заявку!", ignore_case=True), state='*')
async def start_work(message: types.Message, state: FSMContext):
    await state.finish()
    global user_app
    user_app = UserApp()
    await States.choose_type_app.set()
    await bot.send_message(message.from_user.id, "Выберите тип заявки:",
                           reply_markup=make_keyboard(type_app_list))


@dp.message_handler(lambda message: message.text, state=States.choose_type_app)
async def send_message_name(message: types.Message, state: FSMContext):
    user_app.type_app = message.text
    await States.next()
    await bot.send_message(message.from_user.id, "Введите ваше ФИО:", reply_markup=start_btn)


@dp.message_handler(lambda message: message.text, state=States.choose_username)
async def send_message_cab(message: types.Message, state: FSMContext):
    user_app.user_name = message.text
    await States.next()
    await bot.send_message(message.from_user.id, "Введите номер кабинета:")


@dp.message_handler(lambda message: message.text, state=States.choose_cabinet)
async def send_message_device(message: types.Message, state: FSMContext):
    user_app.cabinet = message.text
    await States.next()
    await bot.send_message(message.from_user.id, "Введите проблемное устройство:")


@dp.message_handler(lambda message: message.text, state=States.choose_device)
async def send_message_device(message: types.Message, state: FSMContext):
    user_app.problem_device = message.text
    await States.next()
    await bot.send_message(message.from_user.id, "Опишите проблему:")


@dp.message_handler(lambda message: message.text, state=States.choose_problem_text)
async def send_message_device(message: types.Message, state: FSMContext):
    user_app.problem_text = message.text
    user_app.app_number = generate_app_num()
    await bot.send_message(admin_id, user_app.create_app())
    await bot.send_message(message.from_user.id, "Спасибо! Заявка успешно отправлена!")
    await state.finish()


if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp, skip_updates=True)
