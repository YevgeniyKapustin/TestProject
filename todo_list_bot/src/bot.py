import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram_dialog import setup_dialogs, DialogManager

from config import settings
from dialogs import include_dialogs_router
from dialogs.user.states import UserMenu


async def main():
    bot = Bot(token=settings.TOKEN)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    @dp.message(Command("start"))
    async def start(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(UserMenu.username)

    include_dialogs_router(dp)
    setup_dialogs(dp)
    print('start')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
