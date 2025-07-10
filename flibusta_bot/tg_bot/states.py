from aiogram.fsm.state import State, StatesGroup


class SearchByTitleStates(StatesGroup):
    search_by_title = State()
    book_selected = State()
    choose_download_format = State()
    download_book = State()


class SearchByAuthorStates(StatesGroup):
    search_by_author = State()
    choose_book = State()
