import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Flask-сервер для пинга
app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is alive!", 200


# Асинхронная логика бота
async def start_bot():
    load_dotenv(dotenv_path="token.env")
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Переменная окружения BOT_TOKEN не установлена")

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    router = Router()
    dp.include_router(router)

    @router.message(F.text.contains("Витя"))
    async def handler(message: Message):
        await message.answer_photo(FSInputFile("images/angry_cat.jpg"))

    @router.message(F.text.contains("Виктор"))
    async def handler(message: Message):
        await message.answer_photo(FSInputFile("images/angry_cat_important.jpeg"))

    @router.message(F.text.lower().contains("в отпуск"))
    async def handler(message: Message):
        await message.answer("Отпуск - это состояние души, но тикет сам себя не сделает")

    @router.message(F.text.lower().contains("перекур"))
    async def handler(message: Message):
        await message.answer('Записал перекур в Jira как "исследование дымовых сигналов".')

    @router.message(F.text.lower().contains("лень"))
    async def handler(message: Message):
        await message.answer('Лень — это когда ты читаешь таску и надеешься, что она решится от взгляда.')

    @router.message()
    async def default_handler(message: Message):
        if any(w in message.text.lower() for w in ["ебать", "охуеть", "бля", "блять", "пиздец"]):
            await message.answer_photo(FSInputFile("images/ebat.jpg"))

    await dp.start_polling(bot)


# Запуск Flask-сервера в отдельном потоке
def run_flask():
    app.run(host='0.0.0.0', port=8080)


# Главный запуск
if __name__ == "__main__":
    # Flask — в отдельный поток
    Thread(target=run_flask).start()

    # Запускаем aiogram
    asyncio.run(start_bot())