from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = "APIKEY*****"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["повтори"])
async def urban_message(message):
    await message.answer("повторил")


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью')


@dp.message_handler()
async def all_mesages(message):
    await message.answer("Введите команду /start чтобы начать")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

