from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from crud_functions import get_all_products, add_user, is_included, initiate_db


from crud_functions import initiate_db, add_user, is_included, get_all_products

initiate_db()

api = "API*******"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация'), KeyboardButton(text='Регистрация')],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)


class UserState(StatesGroup):
    username = State()
    email = State()
    registration_age = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Добро пожаловать в магазин спортивного питания.\n"
        "Вы можете зарегистрироваться, чтобы совершать покупки, или сразу начать работу.\n"
        "Выберите действие на клавиатуре.",
        reply_markup=start_menu
    )


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Этот бот помогает приобретать спортивное питание!\nСоздал Шкапа Михаил.')


@dp.message_handler(text='Регистрация')
async def register(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await UserState.username.set()


@dp.message_handler(state=UserState.username)
async def get_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь с таким именем уже существует. Введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите ваш email:")
        await UserState.email.set()


@dp.message_handler(state=UserState.email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите ваш возраст:")
    await UserState.registration_age.set()


@dp.message_handler(state=UserState.registration_age)
async def get_registration_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        data = await state.get_data()
        add_user(data['username'], data['email'], age)
        await message.answer("Регистрация успешно завершена! Теперь вы можете покупать товары.")
        await state.finish()
    except ValueError:
        await message.answer("Возраст должен быть числом!")


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()
    for product_id, title, description, price, image_url in products:
        keyboard = InlineKeyboardMarkup()
        buy_button = InlineKeyboardButton(text="Купить", callback_data=f"buy_{product_id}")
        keyboard.add(buy_button)

        caption = f"Название: {title}\nОписание: {description}\nЦена: {price} руб."
        await message.answer_photo(image_url, caption=caption, reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith("buy_"))
async def handle_buy(call: types.CallbackQuery):
    product_id = call.data.split("_")[1]
    await call.message.answer(f"Вы успешно купили продукт с ID {product_id}!")
    await call.answer()


@dp.message_handler()
async def fallback(message: types.Message):
    await message.answer('Неизвестная команда. Нажмите /start, чтобы начать.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)