from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from pprint import pprint
import asyncio
import requests  # библиотека для генерации запросов

api_crypto = "https://min-api.cryptocompare.com/data/price?"
bot_token = "5179963786:AAFJ2x0BzJKFIebbKIl4ov3AgjXIvsSmWmo"

loop = asyncio.get_event_loop()  # асинхронный цикл

bot = Bot(bot_token)
dp = Dispatcher(bot, loop)


@dp.message_handler(commands="start")
async def start_handler(message: Message):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)  #
    # buttons_list = [KeyboardButton(text="Привет"),KeyboardButton(text="Локация"), KeyboardButton(text="Как дела?")]
    buttons.add(KeyboardButton(text="Привет"))
    buttons.add(KeyboardButton(text="💲 USD 💲"))
    buttons.add(KeyboardButton(text="ETH"))
    buttons.add(KeyboardButton(text="₿ BTC ₿"))

    await message.answer(text="Добро пожаловать!", reply_markup=buttons)


@dp.message_handler()  # декоратор - добавить функционал к функции
async def exo(message: Message):
    if message.text == f"Привет":
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker="CAACAgIAAxkBAAPgYksAASdHnPe1Z3M_20WyeKD16NQOAAJeCQACeVziCdXHsrIrmx2MIwQ")
    elif "usd" in message.text.lower():
        updates = requests.get(api_crypto + "fsym=USD&tsyms=RUB").json()
        await message.answer(text=f"1 USD = {updates['RUB']} RUB")
    elif "eth" in message.text.lower():
        buttons = InlineKeyboardMarkup()
        buttons.add(
            InlineKeyboardButton("USD", callback_data="ETH|USD"),
            InlineKeyboardButton("RUB", callback_data="ETH|RUB"),
            InlineKeyboardButton("EUR", callback_data="ETH|EUR"))
        await message.answer(text="Выберите валюту для конвертации", reply_markup=buttons)
    elif "btc" in message.text.lower():
        buttons = InlineKeyboardMarkup()
        buttons.add(
            InlineKeyboardButton("USD", callback_data="BTC|USD"),
            InlineKeyboardButton("RUB", callback_data="BTC|RUB"),
            InlineKeyboardButton("EUR", callback_data="BTC|EUR"))
        await message.answer(text="Выберите валюту для конвертации", reply_markup=buttons)
    else:
        text = f"Приветствую тебя {message.from_user.first_name}, {message.text}"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_to_message_id=message.message_id)


@dp.callback_query_handler()
async def open(callback: CallbackQuery):
    data = callback.data.split("|")  # [ETH,RUB]
    if data[0] == "ETH":
        updates = requests.get(api_crypto + "fsym=ETH&tsyms=USD,RUB,EUR").json()
        # {'USD': , 'RUB': }
        await bot.send_message(callback.from_user.id, text=f"1 ETH = {updates[data[1]]} {data[1]}")
    elif data[0] == "BTC":
        updates = requests.get(api_crypto + "fsym=BTC&tsyms=USD,RUB,EUR").json()
        await bot.send_message(callback.from_user.id, text=f"1 BTC = {updates[data[1]]} {data[1]}")


executor.start_polling(dp)
