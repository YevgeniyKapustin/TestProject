import requests
from requests import Response


async def check_exist_task(task_id):
    url = f'https://localhost/task/{task_id}/'
    response: Response = requests.get(url)
    return True if response.status_code == 200 else False
