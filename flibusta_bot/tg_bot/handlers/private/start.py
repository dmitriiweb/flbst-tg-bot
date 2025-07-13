from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from fluentogram import TranslatorRunner  # type: ignore
from loguru import logger

from flibusta_bot.tg_bot.filters.i18n_filter import I18nFilter
from flibusta_bot.tg_bot.keyboards.one_column_listing import (
    one_column_listing as start_keyboard,
)
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())
router.callback_query.middleware(TranslatorRunnerMiddleware())


@router.message(CommandStart())
async def cmd_start(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    await state.clear()
    try:
        await message.answer(
            i18n.start.greeting(),
            reply_markup=start_keyboard(
                i18n.start.choose.library.flibusta(),
                i18n.start.choose.library.gutenberg(),
            ),
        )
    except Exception as e:
        logger.error(f"cmd_start error: {e}")
        try:
            await message.answer(i18n.start.error.generic())
        except Exception:
            pass


@router.message(I18nFilter("cancel-button"))
async def cancel(message: Message, state: FSMContext, i18n: TranslatorRunner, **data):
    await state.clear()
    await message.answer(
        i18n.start.choose.action(),
        reply_markup=start_keyboard(
            i18n.start.choose.library.flibusta(),
            i18n.start.choose.library.gutenberg(),
        ),
    )


@router.callback_query(F.data == "back")
async def cancel_callback(callback: CallbackQuery, state: FSMContext, **data):
    i18n = data["i18n"]
    await state.clear()
    if callback.message is None:
        return
    await callback.message.answer(
        i18n.start.choose.action(),
        reply_markup=start_keyboard(
            i18n.start.search.by.title.button(),
            i18n.start.search.by.author.button(),
        ),
    )
