from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    from . import private

    # flibusta handlers
    dp.include_router(private.start_router)
    dp.include_router(private.flibusta_router.start_router)
    dp.include_router(private.flibusta_router.search_by_title_router)
    dp.include_router(private.flibusta_router.search_by_author_router)

    # gutenberg handlers
    dp.include_router(private.gutenberg_router.start_router)


__all__ = ["register_handlers"]
