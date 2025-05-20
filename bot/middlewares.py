import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import SQLAlchemyError

from bot.database import async_session
from bot.models import User

logger = logging.getLogger(__name__)

class SaveUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            # Получаем пользователя из события
            user = getattr(event, "from_user", None)
            if not user:
                return await handler(event, data)

            user_id = user.id
            username = user.username
            full_name = user.full_name

            async with async_session() as session:
                async with session.begin():
                    db_user = await session.get(User, user_id)
                    if not db_user:
                        new_user = User(id=user_id, username=username, full_name=full_name)
                        session.add(new_user)
                        logger.info(f"Новый пользователь добавлен: {user_id}")
                    else:
                        updated = False
                        if db_user.username != username:
                            db_user.username = username
                            updated = True
                        if db_user.full_name != full_name:
                            db_user.full_name = full_name
                            updated = True
                        if updated:
                            await session.commit()
                            logger.info(f"Данные пользователя обновлены: {user_id}")

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при работе с БД: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")

        return await handler(event, data)
