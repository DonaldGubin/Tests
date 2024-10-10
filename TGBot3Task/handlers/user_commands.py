from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
import requests
from handlers.reader_api import config

router = Router()
BASE_URL = "https://v6.exchangerate-api.com/v6"


@router.message(CommandStart())
async def start_cmd(msg: Message):
    await msg.answer("Здравствуйте, это бот для предоставления актуальную информацию о курсе рубля к основным "
                     "валютам. Используйте команду rate [currency], для того чтобы вывести курс валюты относительно к "
                     "RUB, доступные валюты - USD, EUR")


@router.message(Command("rate"))
async def rate(msg: Message, command: CommandObject):
    info = command.args
    if info not in ["EUR", "USD"]:
        await msg.answer("Введите одну из валют - USD/EUR")
        return
    response = requests.get(f"{BASE_URL}/{config.api_key.get_secret_value()}/pair/{info}/RUB")

    try:
        data = response.json()
        if data.get("result") == "success":
            await msg.answer(f"{data.get("conversion_rate")}")
        else:
            print(data)
            await msg.answer("Что то пошло не так")
    except requests.JSONDecodeError:
        await msg.answer(f"Ошибка декодирования JSON: {response.text}")
