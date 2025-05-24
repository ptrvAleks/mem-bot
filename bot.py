import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv


# Загружаем токен из .env или окружения
load_dotenv(dotenv_path="token.env")
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Пожалуйста, установи переменную окружения BOT_TOKEN с токеном бота")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # protect_content=True  # если нужно
    )
)

dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(F.text.contains("Витя"))
async def my_handler(message: Message):
    photo = FSInputFile("images/angry_cat.jpg")
    await message.answer_photo(photo)

@router.message(F.text.contains("Виктор"))
async def my_handler(message: Message):
    photo = FSInputFile("images/angry_cat_important.jpeg")
    await message.answer_photo(photo)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())