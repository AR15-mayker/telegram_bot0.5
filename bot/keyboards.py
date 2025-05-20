from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List, Optional, Union


# === Главное меню (Reply клавиатура) ===
def get_main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        ["📋 Мои задачи", "🎯 Мои привычки"],
        ["➕ Добавить задачу", "➕ Добавить привычку"],
        ["📊 Статистика", "⚙️ Настройки"]
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in buttons],
        resize_keyboard=True
    )


# === Подтверждение действия (Инлайн-клавиатура) ===
def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Клавиатура управления задачей ===
def get_task_control_keyboard(task_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_task_{task_id}"),
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_task_{task_id}")
        ],
        [
            InlineKeyboardButton(text="✅ Выполнено", callback_data=f"done_task_{task_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Клавиатура управления привычкой ===
def get_habit_control_keyboard(habit_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_habit_{habit_id}"),
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_habit_{habit_id}")
        ],
        [
            InlineKeyboardButton(text="✅ Выполнил сегодня", callback_data=f"done_habit_{habit_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Клавиатура выбора поля задачи для редактирования ===
def get_edit_task_fields() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Название", callback_data="edit_title")],
        [InlineKeyboardButton(text="Описание", callback_data="edit_description")],
        [InlineKeyboardButton(text="Дедлайн", callback_data="edit_deadline")],
        [InlineKeyboardButton(text="Категория", callback_data="edit_category")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="cancel_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Клавиатура для настроек пользователя ===
def get_settings_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🌍 Часовой пояс", callback_data="set_timezone")],
        [InlineKeyboardButton(text="🔔 Время напоминаний", callback_data="set_reminder_time")],
        [InlineKeyboardButton(text="🇷🇺 Язык", callback_data="set_language")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Клавиатура для отмены действия ===
def get_cancel_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Простая клавиатура с кнопкой "Отмена" для FSM ===
def get_fsm_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )


# === Клавиатура для выбора дня недели (например, для привычек) ===
def get_weekdays_keyboard(selected_days: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    selected_days = selected_days or []

    buttons = []
    row = []

    for day in days:
        emoji = "✅" if day in selected_days else "❌"
        row.append(InlineKeyboardButton(text=f"{emoji} {day}", callback_data=f"toggle_day_{day}"))
        if len(row) == 3:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="✅ Готово", callback_data="save_weekdays")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
