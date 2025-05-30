from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    from . import user

    dp.include_router(user.router)


__all__ = ["register_handlers"]
