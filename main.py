import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters import Command

from config import TOKEN

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(Command("start"))  # Используем фильтр Command для обработки команд
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Привет")
    builder.button(text="Пока")
    builder.adjust(2)
    await message.answer("Выберите опцию:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/links\n/dynamic")

# Обработчик кнопки "Привет"
@dp.message(F.text == "Привет")  # Используем F для фильтрации текстовых сообщений
async def handle_hello(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Обработчик кнопки "Пока"
@dp.message(F.text == "Пока")
async def handle_bye(message: types.Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Обработчик команды /links
@dp.message(Command("links"))
async def cmd_links(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com/"))
    builder.add(InlineKeyboardButton(text="Музыка", url="https://music.youtube.com/"))
    builder.add(InlineKeyboardButton(text="Видео", url="https://www.youtube.com/"))
    await message.answer("Ссылки:", reply_markup=builder.as_markup())

# Обработчик команды /dynamic
@dp.message(Command("dynamic"))
async def cmd_dynamic(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Показать больше", callback_data="show_more"))
    await message.answer("Опции:", reply_markup=builder.as_markup())

# Обработчик нажатий на инлайн-кнопки
@dp.callback_query(F.data == "show_more")
async def callback_show_more(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Опция 1", callback_data="option_1"))
    builder.add(InlineKeyboardButton(text="Опция 2", callback_data="option_2"))
    await callback.message.edit_text("Выберите опцию:", reply_markup=builder.as_markup())

# Обработчик для опций 1 и 2
@dp.callback_query(F.data.in_({"option_1", "option_2"}))
async def callback_option(callback: types.CallbackQuery):
    option_text = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.message.answer(f"Вы выбрали: {option_text}")

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
