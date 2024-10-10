from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
import requests

router = Router()

ITEMS_PER_PAGE = 100

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать расположение твоего товара\n"
                     "Для этого введи команду /search Категория Артикул\n"
                     "Пример - /search Платье 87989388")


@router.message(Command("search"))
async def start_handler_search(msg: Message, command: CommandObject):
    info = command.args
    query = info.split(' ')[0]  # категория
    article = info.split(' ')[-1]  # артикул

    # артикул состоит только из цифр
    if not article.isdigit():
        await msg.answer("Неправильный формат артикула. Пожалуйста, введите только цифры.")
        return

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
                position = (page - 1) * ITEMS_PER_PAGE + (index + 1)  # Общая позиция товара
                await msg.answer(
                    f"Товар найден на странице {page}, на {index + 1}-м месте (общая позиция: {position}).")
                found = True
                break

        if found:
            break

    if not found:
        await msg.answer("Товар не найден в пределах 50 страниц.")

@router.message()
async def message_handler(msg: Message):
    await msg.answer("Я предназначен только для поискаа товаров\n"
                     "Напиши команду /start")





























#     info = command.args
#     await msg.answer(f"Нашел")
#     response = requests.get(
#         f'https://search.wb.ru/exactmatch/ru/common/v7/search?ab_testing=false&appType=1&curr=rub&dest=123586098&query={info}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false')
#     products = response.json().get('data').get('products')
#     for product in products:
#         if product.get('id') == int(info.split(' ')[-1]):
#             await msg.answer(f'вот расположение {product}')
#     print(response.json())
#
#
# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer("Я предназначен только для поискаа товаров\n"
#                      "Напиши команду /start")

