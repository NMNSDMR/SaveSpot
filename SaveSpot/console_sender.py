import asyncio
from aiogram import Bot

TOKEN = "broo))"

async def console_bot():
    bot = Bot(token=TOKEN)
    print("💬 Консольный чат-бот запущен!")
    print("👉 Формат ввода: <chat_id> <текст сообщения>")
    print("   Пример: 123456789 Привет! Это бот из терминала.")
    print("   Чтобы выйти, введи: exit\n")

    while True:
        try:
            line = input(">>> ").strip()
            if not line:
                continue
            if line.lower() in {"exit", "quit"}:
                print("👋 Завершение работы.")
                break

            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                print("⚠️  Ошибка: укажи chat_id и текст через пробел.")
                continue

            chat_id_str, text = parts
            chat_id = int(chat_id_str)

            await bot.send_message(chat_id=chat_id, text=text)
            print(f"✅ Отправлено пользователю {chat_id}: {text!r}")

        except ValueError:
            print("⚠️  Неверный формат chat_id (должно быть число).")
        except Exception as e:
            print(f"❌ Ошибка при отправке: {e}")

if __name__ == "__main__":
    asyncio.run(console_bot())
