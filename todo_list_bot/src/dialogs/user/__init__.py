from aiogram_dialog import Dialog

from dialogs.user import windows
from dialogs.user.utils import add_user


def user_dialogs():
    return [
        Dialog(
            windows.login_input(),
            windows.password_input(),
            on_close=add_user
        ),
    ]
