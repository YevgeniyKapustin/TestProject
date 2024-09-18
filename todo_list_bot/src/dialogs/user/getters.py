from aiogram_dialog import DialogManager


async def get_user_data(dialog_manager: DialogManager, **middleware_data):
    return {
        'username': dialog_manager.find('username').get_value(),
        'password': dialog_manager.find('password').get_value(),
    }
