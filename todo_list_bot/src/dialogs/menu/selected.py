from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dialogs.menu.states import BotMenu


async def on_chosen_task(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(task_id=item_id)
    await manager.switch_to(BotMenu.select_tasks)
