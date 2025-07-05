from aiogram.fsm.state import State, StatesGroup


class SearchByTitleStates(StatesGroup):
    search_by_title = State()


class SearchByAuthorStates(StatesGroup):
    search_by_author = State()