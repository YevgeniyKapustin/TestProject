from aiogram import Dispatcher

from dialogs import user


def include_dialogs_router(dp: Dispatcher):
    for dialog in [*user.user_dialogs()]:
        dp.include_router(dialog)
