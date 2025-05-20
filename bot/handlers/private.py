from aiogram import Router, F
from aiogram.types import Message

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("Привет! Я помогу тебе планировать задачи!")
