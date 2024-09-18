from aiogram_dialog import Dialog

from dialogs.menu import windows


def menu_dialogs():
    return [
        Dialog(
            windows.task_window(),
            on_process_result=windows.on_process_result,
        ),
    ]
