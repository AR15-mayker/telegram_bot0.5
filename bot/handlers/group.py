from aiogram import Router, F
from aiogram.types import Message

router = Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message()
async def group_message_handler(message: Message):
    if any(word in message.text.lower() for word in ["плохое_слово1", "плохое_слово2"]):
        await message.delete()
        await message.answer("Мат запрещён!")
