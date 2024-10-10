import re
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
import requests

router = Router()

ITEMS_PER_PAGE = 100

SEARCH_PATTERN = re.compile(r"(.+)\s(\d+)$")  

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать расположение твоего товара\n"
                     "Для этого введи команду /search Категория Артикул\n"
                     "Пример - /search Платье 87989388")


@router.message(Command("search"))
async def start_handler_search(msg: Message, command: CommandObject):
    try:
        info = command.args
        if not info:
            raise ValueError("Отсутствуют аргументы. Введите запрос в формате: /search Категория Артикул")

        match = SEARCH_PATTERN.match(info)
        if not match:
            raise ValueError(
                "Неверный формат запроса. Введите запрос в формате: /search Категория Артикул\nПример: /search Платье 87989388")

        query, article = match.groups()

        if not article.isdigit():
            raise ValueError("Неправильный формат артикула. Пожалуйста, введите только цифры.")

        found = False
        article = int(article)

        # 50 страниц (по 100 товаров на каждой)
        for page in range(1, 51):
            response = requests.get(
                f'https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=123586098&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&page={page}'
            )
            products = response.json().get('data', {}).get('products', [])

            if not products:
                await msg.answer("Товар не найден.")
                return


            for index, product in enumerate(products):
                if product.get('id') == article:
                    position = (page - 1) * ITEMS_PER_PAGE + (index + 1)  # Общая позиция
                    await msg.answer(
                        f"Товар найден на странице {page}, на {index + 1}-м месте (общая позиция: {position}).")
                    found = True
                    break

            if found:
                break

        if not found:
            await msg.answer("Товар не найден в пределах 50 страниц.")

    except ValueError as e:
        await msg.answer(f"Ошибка: {e}")
    except Exception as e:
        await msg.answer(f"Произошла ошибка: {e}")


@router.message()
async def message_handler(msg: Message):
    await msg.answer("Я предназначен только для поиска товаров\n"
                     "Напиши команду /start")