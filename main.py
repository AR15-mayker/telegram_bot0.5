import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Импорты из bot/
from bot.config import BOT_TOKEN
from bot.handlers import private, group, channel
from bot.database import init_db
from bot.middlewares import LoggingMiddleware, AccessMiddleware, SaveUserMiddleware, ExecutionTimeMiddleware


async def main():
    # Логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        filename="logs/bot.log",
        filemode="a"
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot...")

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # === Подключение мидлварей ===

    # Получаем список разрешённых пользователей (можно загрузить из БД или .env)
    allowed_users = [123456789]  # Замените на реальный ID администратора или список

    # Логирование событий
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    # Автоматическое сохранение информации о пользователе
    dp.message.middleware(SaveUserMiddleware())
    dp.callback_query.middleware(SaveUserMiddleware())

    # Проверка доступа
    dp.message.middleware(AccessMiddleware(allowed_users))
    dp.callback_query.middleware(AccessMiddleware(allowed_users))

    # Измерение времени выполнения
    dp.message.middleware(ExecutionTimeMiddleware())

    # === Инициализация базы данных ===
    await init_db()

    # === Регистрация роутеров ===
    dp.include_router(private.router)   # Личные сообщения
    dp.include_router(group.router)     # Групповые чаты
    dp.include_router(channel.router)   # Каналы

    # === Запуск бота ===
    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
