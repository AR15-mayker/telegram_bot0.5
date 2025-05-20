import aiohttp
import asyncio
from typing import Optional, Dict, List

# Примеры API для интеграции
QUOTES_API_URL = "https://api.quotable.io/random "
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks "
TODOIST_API_TOKEN = "ваш_токен_todoist"  # Укажите в .env


async def get_motivational_quote() -> Optional[Dict[str, str]]:
    """
    Получает случайную мотивационную цитату с сайта quotable.io.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(QUOTES_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "author": data["author"],
                        "quote": data["content"]
                    }
                else:
                    print(f"Ошибка получения цитаты: {response.status}")
                    return None
    except Exception as e:
        print(f"Исключение при получении цитаты: {e}")
        return None


async def sync_task_with_todoist(task_data: dict) -> bool:
    """
    Синхронизирует задачу с Todoist через REST API.
    task_data должен содержать заголовок и, опционально, описание, дедлайн и т.д.
    """
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(TODOIST_API_URL, json=task_data, headers=headers) as resp:
                if resp.status == 200 or resp.status == 201:
                    print("Задача успешно добавлена в Todoist")
                    return True
                else:
                    error_text = await resp.text()
                    print(f"Ошибка добавления в Todoist: {resp.status} - {error_text}")
                    return False
    except Exception as e:
        print(f"Ошибка при подключении к Todoist: {e}")
        return False


async def fetch_weather(city: str, api_key: str) -> Optional[Dict]:
    """
    Пример функции для получения погоды (при необходимости).
    """
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(weather_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "city": city,
                        "temp": data["current"]["temp_c"],
                        "condition": data["current"]["condition"]["text"]
                    }
                else:
                    print(f"Ошибка получения погоды: {response.status}")
                    return None
    except Exception as e:
        print(f"Исключение при получении погоды: {e}")
        return None


def format_daily_report(tasks: List[dict], habits: List[dict]) -> str:
    """
    Форматирует ежедневный отчет по задачам и привычкам.
    """
    report = "<b>Ежедневный отчёт:</b>\n\n"

    report += "<b>Задачи:</b>\n"
    for task in tasks:
        status = "✅" if task.get("done") else "❌"
        report += f"{status} {task['title']} ({task.get('deadline', 'нет')})\n"

    report += "\n<b>Привычки:</b>\n"
    for habit in habits:
        status = "✅" if habit.get("completed_today") else "❌"
        report += f"{status} {habit['name']} | Стрик: {habit['streak']}\n"

    return report


if __name__ == "__main__":
    # Тестирование асинхронных функций
    async def test():
        quote = await get_motivational_quote()
        print("Цитата:", quote)

        # Пример синхронизации с Todoist
        task = {
            "content": "Тестовая задача из бота",
            "description": "Это тестовая задача, созданная через Python",
            "due_string": "tomorrow at 10:00"
        }
        result = await sync_task_with_todoist(task)
        print("Todoist sync success:", result)

    asyncio.run(test())
