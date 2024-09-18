import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 6


def paginated_tasks(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='s_scroll_tasks',
            item_id_getter=operator.itemgetter(1),
            items='tasks',
            on_click=on_click,
        ),
        id='tasks_ids',
        width=1,
        height=SCROLLING_HEIGHT,
    )
