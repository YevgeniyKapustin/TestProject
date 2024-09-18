import requests
from aiogram_dialog import DialogManager
from requests import Response

from config import settings


async def get_tasks(dialog_manager: DialogManager, **middleware_data):
    url = f'{settings.TODO_BACKEND_URL}/tasks'

    response: Response = requests.get(url, headers={'Authorization': 'Bearer'})

    tasks: dict = response.json()

    data = {
        'tasks': [
            (f'{task.name}', task.task_id)
            for task in tasks
        ],
    }
    return data
