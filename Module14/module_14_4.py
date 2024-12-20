from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import asyncio
from crud_functions import get_all_products, initiate_db

initiate_db()

api = "7481324612:AAFo4k99IxVuILJVdrSL_orVlAlK9VM47Ig"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация'), KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Жми кнопку рассчитать или купить продукт.", reply_markup=start_menu)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Бота создал Шкапа Михаил!')

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    bmr = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Ваша норма калорий: {bmr:.2f}")

    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    product_kb = InlineKeyboardMarkup()
    for title, description, price, image_url in products:
        caption = f"Название: {title} | Описание: {description} | Цена: {price}"
        await message.answer_photo(image_url, caption=caption)
        product_kb.add(InlineKeyboardButton(text=title, callback_data=f"product_{title.lower()}"))
    await message.answer("Выберите продукт для покупки:", reply_markup=product_kb)

@dp.callback_query_handler(Text(startswith="product_"))
async def send_confirm_message(call):
    product_name = call.data.split('_')[1].capitalize()
    await call.message.answer(f"Вы успешно приобрели {product_name}!")
    await call.answer()

@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    formula = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (годы) + 5\n"
        "Для женщин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (годы) − 161"
    )
    await call.message.answer(formula)
    await call.answer()

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введи команду /start чтобы начать')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
