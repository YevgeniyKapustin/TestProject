from aiogram.fsm.state import StatesGroup, State


class BotMenu(StatesGroup):
    select_tasks = State()
