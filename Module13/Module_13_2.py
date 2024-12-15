from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "APIKEY*******"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text = ["nd"])
async def urban_message(message):
    print("090909")


@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Привет! Я бот помогающий твоему здоровью')


@dp.message_handler()
async def all_mesages(message):
    print("Введите команду /start чтобы начать")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)