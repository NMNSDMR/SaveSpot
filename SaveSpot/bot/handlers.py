from aiogram import types
from bot.database import add_user, add_tag, get_tags, get_last_location, get_location_history

async def cmd_where(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("📍 Пример: /where ABC123")
        return
    tag = parts[1].strip().upper()
    loc = await get_last_location(tag)
    if not loc:
        await message.answer(f"❌ Нет данных о метке {tag}")
    else:
        lat, lon, ts = loc
        await message.answer(f"📦 Метка {tag}\n🕒 {ts}")
        await message.answer_location(latitude=lat, longitude=lon)


async def cmd_history(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        await message.answer("🗺 Пример: /history ABC123")
        return
    tag = parts[1].strip().upper()
    history = await get_location_history(tag, limit=10)
    if not history:
        await message.answer(f"❌ История для {tag} пуста.")
    else:
        text = f"📜 История {tag}:\n"
        for lat, lon, ts in history:
            text += f"• {ts}: {lat}, {lon}\n"
        await message.answer(text)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
tag_code = "ВАВ123"
async def cmd_start(message: types.Message):
    await add_user(message.from_user.id)

    keyboard = InlineKeyboardMarkup()

    await message.answer(
        "👋 Привет! Я бот для отслеживания вещей.\n\n"
        "Отправь /add <код_метки>, чтобы зарегистрировать NFC-метку.\n"
        "Отправь /mytags, чтобы увидеть список твоих меток.\n",
        reply_markup=keyboard
    )

async def cmd_add(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("❌ Укажи код метки, пример: /add ABC123")
        return
    tag_code = parts[1].strip().upper()
    await add_tag(message.from_user.id, tag_code)
    await message.answer(f"✅ Метка {tag_code} добавлена!")

async def cmd_mytags(message: types.Message):
    tags = await get_tags(message.from_user.id)
    if not tags:
        await message.answer("📭 У тебя пока нет зарегистрированных меток.")
    else:
        text = "📦 Твои метки:\n" + "\n".join(f"• {t}" for t in tags)
        await message.answer(text)
async def cmd_history(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        await message.answer("🗺 Пример: /history ABC123")
        return
    tag = parts[1].strip().upper()
    history = await get_location_history(tag, limit=10)
    if not history:
        await message.answer(f"❌ История для {tag} пуста.")
    else:
        text = f"📜 История {tag}:\n"
        for lat, lon, ts in history:
            text += f"• {ts}: {lat}, {lon}\n"
        await message.answer(text)
