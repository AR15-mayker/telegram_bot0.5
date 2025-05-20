from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def on_channel_join(event: ChatMemberUpdated):
    await event.answer("Спасибо за добавление в канал!")


@router.message(F.chat.type == "channel")
async def channel_post_handler(message: Message):
    print(f"Получен пост из канала: {message.text}")
