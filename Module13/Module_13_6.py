from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import asyncio

api = "APIKEY**************"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# kb=ReplyKeyboardMarkup()
# button1 = KeyboardButton(text='Информация')
# button2 = KeyboardButton(text='Рассчитать')
# kb.add(button1, button2)

in_kb = InlineKeyboardMarkup()
inbtn_calories = InlineKeyboardButton(text='Рассчитать', callback_data='calories')
inbtn_formula = InlineKeyboardButton(text='Формула', callback_data='formula')
in_kb.add(inbtn_calories, inbtn_formula)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Рассчитать')]
    ], resize_keyboard=True
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Жми кнопку рассчитать", reply_markup=start_menu)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Бота создал Шкапа Михаил!')



@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=in_kb)


@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    formula = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для мужчин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (годы) + 5\n"
        "Для женщин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (годы) − 161"
    )
    await call.message.answer(formula)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
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

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введи команду /start чтобы начать')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)