from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.client.default import DefaultBotProperties
import asyncio
import os
import time

from config import BOT_TOKEN
from style_processor import stylize_image


# Инициализируем бота и диспетчер
bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

    
dp = Dispatcher(storage=MemoryStorage())

# Основная клавиатура
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎨 Обработать изображение")],
        [KeyboardButton(text="💳 Купить обработки"), KeyboardButton(text="📊 Баланс")],
        [KeyboardButton(text="❓ Помощь")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

 
# Кнопки выбора стиля
style_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Дисней", callback_data="style_disney")],
        [InlineKeyboardButton(text="🌸 Гибли", callback_data="style_ghibli")],
        [InlineKeyboardButton(text="💛 Симпсоны", callback_data="style_simpsons")],
        [InlineKeyboardButton(text="🎭 South Park", callback_data="style_southpark")],
        [InlineKeyboardButton(text="🕶 Киберпанк 2077", callback_data="style_cyberpunk")],
        [InlineKeyboardButton(text="🎨 Ван Гог", callback_data="style_vangogh")]
    ]
)

# Кнопки выбора формата
format_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌁 Квадрат 1:1, 1024х1024", callback_data="format_1024x1024")],
        [InlineKeyboardButton(text="🖥️ Горизонтальный 16:9, 1792х1024", callback_data="format_1792x1024")],
        [InlineKeyboardButton(text="📱 Вертикальный 9:16, 1024х1792", callback_data="format_1024x1792")]
    ]
)

# Временное хранилище данных по пользователям
# Здесь будем хранить {user_id: {"image_path": ..., "style": ...}}
user_sessions = {}

# Обработчик /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}!\n\n"
        "Я - бот, который превращает Ваши фотографии в стиль популярных художников и мультфильмов.\n\n"
        "🎁 Вы можете бесплатно обработать 3 изображения в день.\n"
        "💡 Хотите больше? Выберите подходящий тариф.\n\n"
        "Нажмите кнопку ниже, чтобы начать 👇",
        reply_markup=main_kb
    )

# Прием фото от пользователя
@dp.message(F.photo)
async def handle_photo(message: Message):
    user_id = message.from_user.id
   # await message.answer("📷 Фото получено! Выберите стиль обработки:", reply_markup=style_buttons)

    # Сохраняем фото во временный файл
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = f"temp/{user_id}_{int(time.time())}.jpg"
    await bot.download_file(file.file_path, destination=file_path)

    # Запоминаем путь к изображению
    user_sessions[user_id] = {"image_path": file_path}

    await message.answer("📷 Фото получено! Теперь выберите стиль обработки:", reply_markup=style_kb)


# Обработка выбора стиля
@dp.callback_query(F.data.startswith("style_"))
async def handle_style(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    style_key = callback.data.replace("style_", "")
     #style = callback.data.replace("style_", "")
   # await callback.message.answer(f"Вы выбрали стиль: <b>{style.capitalize()}</b>\nСкоро здесь появится Ваша обработка...")
   # await callback.answer()

    # Запоминаем стиль
    if user_id in user_sessions:
        user_sessions[user_id]["style"] = style_key
        await callback.message.answer("✅ Стиль выбран! Теперь выберите формат изображения:", reply_markup=format_kb)
    else:
        await callback.message.answer("❗ Пожалуйста, сначала отправьте изображение.")

    await callback.answer()

# Обработка выбора формата и генерация изображения
@dp.callback_query(F.data.startwith("format_"))
async def handle_format(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    format_size = callback.data.replace("format_", "")

    if user_id not in user_sessions or "style" not in user_sessions[user_id]:
        await callback.message.answer("❗ Сначала отправьте фото и выберите стиль.")
        await callback.answer()
        return

    session = user_sessions[user_id]
    image_path = session["image_path"]
    style = session["style"]

    await callback.message.answer("🎨 Обрабатываю изображение... Это может занять до 5 минут.")

    # Запускаем обработку
    result_url = await stylize_image(image_path, style, format_size)

    if result_url:
        await callback.message.answer_photo(photo=result_url, caption="✅ Готово! Вот ваше изображение.")
    else:
        await callback.message.answer("❗ Произошла ошибка при генерации изображения. Попробуйте позже.")

    # Удаляем временные файлы (по желанию)
    try:
        os.remove(image_path)
    except:
        pass

    # Сбросим сессию пользователя
    user_sessions.pop(user_id, None)

    await callback.answer()




   






# Запук
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
