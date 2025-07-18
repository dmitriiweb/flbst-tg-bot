from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner  # type: ignore

from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.filters.i18n_filter import I18nFilter
from flibusta_bot.tg_bot.keyboards import cancels as cancels_keyboard
from flibusta_bot.tg_bot.keyboards.one_column_listing import one_column_listing
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())
router.callback_query.middleware(TranslatorRunnerMiddleware())


@router.message(I18nFilter("start-choose-library-gutenberg"))
async def choose_library_gutenberg(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    answer = i18n.gutetenberg.call.to.action()
    await message.answer(answer)
