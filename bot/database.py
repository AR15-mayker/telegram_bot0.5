from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

from bot.config import DATABASE_URL

# Логгирование
logger = logging.getLogger(__name__)

# Создание базового класса модели
Base = declarative_base()

# Создание асинхронного движка (engine)
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    """
    Создает все таблицы в БД.
    """
    try:
        async with engine.begin() as conn:
            # Создаем все таблицы
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Таблицы успешно созданы.")
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
