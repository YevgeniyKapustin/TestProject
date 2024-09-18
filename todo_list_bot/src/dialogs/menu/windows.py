from typing import Any

from aiogram_dialog import Window, Data, DialogManager, ShowMode
from aiogram_dialog.widgets.text import Const

from dialogs.menu import keyboards, getters, selected
from dialogs.menu.states import BotMenu


def task_window():
    return Window(
        Const('Выберите задачу для просмотра'),
        keyboards.paginated_tasks(selected.on_chosen_task),
        state=BotMenu.select_tasks,
        getter=getters.get_tasks
    )


async def on_process_result(data: Data, result: Any, manager: DialogManager):
    if result:
        print('здарова')
        #switch_to_window = result.get('switch_to_window')
        #await manager.switch_to(BotMenu.select_products)
