from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Const

from dialogs.user.states import UserMenu


def login_input():
    return Window(
        Const('Введите логин'),
        TextInput(id='username', on_success=Next()),
        state=UserMenu.username
    )


def password_input():
    return Window(
        Const('Введите пароль'),
        TextInput(id='password', on_success=Next()),
        state=UserMenu.password
    )
