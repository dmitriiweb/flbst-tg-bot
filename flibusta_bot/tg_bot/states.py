from aiogram.fsm.state import State, StatesGroup


class FlibustaSearchByTitleStates(StatesGroup):
    search_by_title = State()
    book_selected = State()
    choose_download_format = State()
    download_book = State()


class FlibustaSearchByAuthorStates(StatesGroup):
    search_by_author = State()
    choose_book = State()


class GutenbergStartStates(StatesGroup):
    search_query = State()
    download_book = State()
