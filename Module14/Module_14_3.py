from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import asyncio

api = "APIKEY************"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

product_kb = InlineKeyboardMarkup()
products = ["Product1", "Product2", "Product3", "Product4"]
for product in products:
    product_kb.add(InlineKeyboardButton(text=product, callback_data=f"product_{product.lower()}"))

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
    descriptions = [
        "Название: Product1 | Описание: описание 1 | Цена: 100",
        "Название: Product2 | Описание: описание 2 | Цена: 200",
        "Название: Product3 | Описание: описание 3 | Цена: 300",
        "Название: Product4 | Описание: описание 4 | Цена: 400"
    ]
    images = [
        "https://biotus.kz/kreatin-monogidrat-creatine-monohydrate-biotech-usa-300-g.html",
        "https://one-win.ru/catalog/kreatin/monogidrat/1win_kreatin_monogidrat_creatine_monohydrate_vkus_malina_30_portsiy/",
        "https://one-win.ru/catalog/kreatin/monogidrat/1win_kreatin_monogidrat_creatine_monohydrate_vkus_malina_30_portsiy/",
        "https://spartapro.ru/sportivnoe-pitanie/gejnery/true-mass-575-lb-bsn"
    ]

    for desc, img in zip(descriptions, images):
        await message.answer_photo(img, caption=desc)

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

