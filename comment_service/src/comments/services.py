from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from comments.models import Comment


class CommentCRUD(object):
    """Класс описывающий поведение команд."""
    __slots__ = ('__id', '__task_id', '__text')

    def __init__(
            self,
            id_: int = None,
            task_id: str = None,
            text: str = None
    ):
        self.__id: int = id_
        self.__task_id: str = task_id
        self.__text: str = text

    async def create(self, session) -> bool:
        """Создание объекта в базе данных."""
        if self.__text and self.__task_id:
            session.add(
                Comment(
                    text=self.__text,
                    task_id=self.__task_id,
                )
            )
            return True
        return False

    async def get(self, session: AsyncSession) -> list | None:
        """Чтение объекта из базы данных."""
        if self.__task_id:
            query = (
                select(Comment).
                where(Comment.task_id == self.__task_id)
            )
        result = session.execute(query)
        return list(result.scalars().all())

    async def update(self, new_obj: dict, session: AsyncSession) -> bool:
        """Обновление объекта в базы данных."""
        self.__task_id = new_obj.get('task_id')
        self.__text = new_obj.get('text')
        objs = await self.get(session)
        if len(objs) >= 1 and (obj := objs[0]):
            obj.task_id = self.__task_id
            obj.text = self.__text

            session.add(obj)
            return True
        return False

    async def delete(self, session: AsyncSession) -> bool:
        """Удаление объекта из базы данных."""
        [await session.delete(obj) for obj in await self.get(session)]
        return True
