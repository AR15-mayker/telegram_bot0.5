from datetime import datetime, timedelta
from typing import Optional, List, Union
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def validate_date(date_str: str) -> Optional[datetime]:
    """
    Проверяет корректность введенной даты.
    Поддерживаемые форматы: 'YYYY-MM-DD', 'DD.MM.YYYY', 'tomorrow', 'today'.
    """
    date_str = date_str.strip().lower()

    if date_str == "сегодня":
        return datetime.now()
    elif date_str == "завтра":
        return datetime.now() + timedelta(days=1)

    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def format_task(task: dict) -> str:
    """
    Форматирует вывод информации о задаче.
    """
    title = task.get("title", "Без названия")
    description = task.get("description", "Нет описания")
    deadline = task.get("deadline", "Не указано")
    done = "✅" if task.get("done") else "❌"

    return (
        f"<b>{title}</b>\n"
        f"{description}\n"
        f"📅 Дедлайн: {deadline}\n"
        f"Статус: {done}"
    )


def generate_inline_keyboard(buttons: List[dict]) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру из списка словарей.
    Пример buttons: [{"text": "Да", "callback_data": "yes"}, {"text": "Нет", "callback_data": "no"}]
    """
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for btn in row:
            keyboard_row.append(InlineKeyboardButton(text=btn["text"], callback_data=btn["callback_data"]))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def generate_reply_keyboard(buttons: List[List[str]], resize_keyboard=True) -> ReplyKeyboardMarkup:
    """
    Создаёт обычную (reply) клавиатуру.
    Пример buttons: [["Добавить задачу", "Мои задачи"], ["Настройки"]]
    """
    keyboard = [[KeyboardButton(text=text) for text in row] for row in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=resize_keyboard)


async def send_daily_reminder(bot, user_id: int, message: str):
    """
    Отправляет пользователю ежедневное напоминание.
    """
    try:
        await bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")


def calculate_streak(last_done: Optional[datetime], today: datetime = None) -> int:
    """
    Рассчитывает стрик привычки на основе последнего выполнения.
    """
    if not last_done:
        return 0

    if today is None:
        today = datetime.now()

    delta_days = (today.date() - last_done.date()).days

    if delta_days == 0:
        return 1  # Выполнено сегодня
    elif delta_days == 1:
        return 2  # Выполнялось вчера
    else:
        return 0  # Стрейк прерван


def get_week_range(date: datetime) -> tuple:
    """
    Возвращает даты начала и конца недели для заданной даты.
    """
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week


def parse_time(time_str: str) -> Optional[datetime.time]:
    """
    Парсит время из строки в формате HH:MM.
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None


def prepare_user_statistics(tasks: list, habits: list) -> str:
    """
    Генерирует текст статистики пользователя.
    """
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.get("done"))
    total_habits = len(habits)
    active_habits = sum(1 for h in habits if h.get("enabled"))

    stats = (
        f"<b>📊 Ваша статистика:</b>\n\n"
        f"📌 Задач всего: {total_tasks}\n"
        f"✅ Завершённых: {completed_tasks}\n"
        f"🔥 Активных привычек: {active_habits} / {total_habits}"
    )
    return stats


def get_default_menu():
    """
    Возвращает стандартное меню для пользователя.
    """
    buttons = [
        ["📋 Мои задачи", "🎯 Мои привычки"],
        ["➕ Добавить задачу", "➕ Добавить привычку"],
        ["📊 Статистика", "⚙️ Настройки"]
    ]
    return generate_reply_keyboard(buttons)