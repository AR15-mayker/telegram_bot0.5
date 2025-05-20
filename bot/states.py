from aiogram.fsm.state import State, StatesGroup


# === Группа состояний для добавления задачи ===
class TaskForm(StatesGroup):
    title = State()         # Название задачи
    description = State()   # Описание задачи
    deadline = State()      # Дедлайн (дата)
    category = State()      # Категория задачи
    confirm = State()       # Подтверждение перед сохранением


# === Группа состояний для добавления привычки ===
class HabitForm(StatesGroup):
    name = State()          # Название привычки
    description = State()   # Описание привычки
    frequency = State()     # Частота выполнения (ежедневно/раз в неделю и т.д.)
    start_date = State()    # Дата начала отслеживания
    confirm = State()       # Подтверждение перед сохранением


# === Группа состояний для поиска/редактирования задачи ===
class EditTask(StatesGroup):
    choose_task = State()   # Выбор задачи для редактирования
    edit_field = State()    # Выбор поля для изменения
    new_value = State()     # Ввод нового значения


# === Группа состояний для настроек пользователя ===
class SettingsForm(StatesGroup):
    timezone = State()      # Выбор часового пояса
    daily_reminder = State()  # Настройка времени ежедневного напоминания
    language = State()      # Выбор языка интерфейса


# === Группа состояний для создания поста канала ===
class ChannelPostForm(StatesGroup):
    content = State()       # Текст поста
    media = State()         # Медиа (изображение, видео, документ)
    schedule = State()      # Время публикации (опционально)
    confirm = State()       # Подтверждение перед отправкой
