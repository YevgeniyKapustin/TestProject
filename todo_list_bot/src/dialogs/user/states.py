from aiogram.fsm.state import StatesGroup, State


class UserMenu(StatesGroup):
    username = State()
    password = State()
