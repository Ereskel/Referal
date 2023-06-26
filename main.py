# Запуск бота и уведомление об этом администраторов. Логгинг.
import asyncio
import logging

from aiogram.types import Message

from config import admins
from loader import dp, bot
from handlers import router


async def notify(bot):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Бот запущен')


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    await notify(bot)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
