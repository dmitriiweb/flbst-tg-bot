from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluentogram import TranslatorRunner  # type: ignore

from flibusta_bot.tg_bot import states as bot_states
from flibusta_bot.tg_bot.filters.i18n_filter import I18nFilter
from flibusta_bot.tg_bot.keyboards.flibusta import cancels as cancels_keyboard
from flibusta_bot.tg_bot.keyboards.flibusta import one_column_listing
from flibusta_bot.tg_bot.middlewares.i118n import TranslatorRunnerMiddleware

router = Router()
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.message.middleware(TranslatorRunnerMiddleware())
router.callback_query.middleware(TranslatorRunnerMiddleware())


@router.message(I18nFilter("start-choose-library-flibusta"))
async def choose_library_flibusta(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    answer = i18n.start.choose.action()
    kb = one_column_listing(
        i18n.start.search.by.title.button(),
        i18n.start.search.by.author.button(),
        i18n.cancel.button(),
    )
    await message.answer(answer, reply_markup=kb)


@router.message(I18nFilter("start-search-by-title-button"))
async def search_by_title(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    await state.set_state(bot_states.FlibustaSearchByTitleStates.search_by_title)
    await message.answer(
        i18n.start.enter.title(),
        reply_markup=cancels_keyboard.single_cansel_kb(i18n.cancel.button()),
    )


@router.message(I18nFilter("start-search-by-author-button"))
async def search_by_author(
    message: Message, state: FSMContext, i18n: TranslatorRunner, **data
):
    await state.set_state(bot_states.FlibustaSearchByAuthorStates.search_by_author)
    await message.answer(
        i18n.start.enter.author(),
        reply_markup=cancels_keyboard.single_cansel_kb(i18n.cancel.button()),
    )
