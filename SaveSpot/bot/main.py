import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot import handlers
from bot.database import init_db

TOKEN = "YOUR TOKEN BRo)"

logger = logging.getLogger("tracker")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            m = update.message
            user = m.from_user
            text = m.text or m.caption or "<no-text>"
            loc = None
            if m.location:
                loc = (m.location.latitude, m.location.longitude)
            logger.info(
                f"IN  <-- user_id={user.id} username={getattr(user,'username',None)} "
                f"name={getattr(user,'first_name','')} chat_id={m.chat.id} "
                f"message_id={m.message_id} text={text!r} location={loc}"
            )
        elif update.callback_query:
            cq = update.callback_query
            user = cq.from_user
            logger.info(
                f"IN  <-- callback_query user_id={user.id} username={getattr(user,'username',None)} "
                f"chat_id={cq.message.chat.id if cq.message else None} data={cq.data!r}"
            )
        else:
            logger.info(f"IN  <-- update type={type(update)} content={update}")

_orig_send_message = Bot.send_message
_orig_send_location = Bot.send_location

async def _logged_send_message(self, chat_id, text, *args, **kwargs):
    logger.info(f"OUT --> chat_id={chat_id} text={text!r}")
    return await _orig_send_message(self, chat_id, text, *args, **kwargs)

async def _logged_send_location(self, chat_id, latitude, longitude, *args, **kwargs):
    logger.info(f"OUT --> send_location chat_id={chat_id} lat={latitude} lon={longitude}")
    return await _orig_send_location(self, chat_id, latitude, longitude, *args, **kwargs)

Bot.send_message = _logged_send_message
Bot.send_location = _logged_send_location

async def on_startup(dp: Dispatcher):
    await init_db()
    logger.info("База данных инициализирована ✅")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handlers.cmd_start, commands=["start"])
    dp.register_message_handler(handlers.cmd_add, commands=["add"])
    dp.register_message_handler(handlers.cmd_mytags, commands=["mytags"])
    dp.register_message_handler(handlers.cmd_where, commands=["where"])
    dp.register_message_handler(handlers.cmd_history, commands=["history"])
    
    # Подсказки тегов
    dp.register_message_handler(show_tags, commands=["tags"])
    dp.register_callback_query_handler(process_where_callback, lambda c: c.data and c.data.startswith("where:"))

def make_tag_keyboard(tags: list[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for tag in tags:
        kb.add(InlineKeyboardButton(text=tag, callback_data=f"where:{tag}"))
    return kb

async def show_tags(message: types.Message):
    tags = ["KLE472", "GHW598", "POQ789", "QWE623", "MSC834"]
    kb = make_tag_keyboard(tags)
    await message.answer("Выбери тег:", reply_markup=kb)

async def process_where_callback(callback_query: CallbackQuery):
    tag = callback_query.data.split(":", 1)[1]
    await callback_query.message.answer(f"/where {tag}")
    await callback_query.answer()  

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())

    register_handlers(dp)
    await on_startup(dp)

    logger.info("Бот запущен 🚀")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
