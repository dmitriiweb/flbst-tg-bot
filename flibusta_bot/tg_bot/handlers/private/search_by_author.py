from aiogram import F, Router
from aiogram.enums import ChatType

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
