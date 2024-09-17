import requests
from requests import Response

from config import settings


async def check_exist_task(task_id) -> bool:
    url = f'{settings.BACKEND_URL}/task/{task_id}/'
    response: Response = requests.get(url)
    return True if response.status_code == 200 else False
