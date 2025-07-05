from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    from . import private

    dp.include_router(private.start_router)
    dp.include_router(private.search_by_title_router)


__all__ = ["register_handlers"]
