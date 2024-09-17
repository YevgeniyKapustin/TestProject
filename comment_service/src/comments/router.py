from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from comments.schemas import CommentScheme, NotFoundScheme
from comments.services import CommentCRUD
from database import get_db

router = APIRouter(
    prefix='/api/v1',
    tags=['Команды'],
)


@router.get(
    '/commands',
    name='Возвращает информацию о команде',
    description='''
    Предоставляет список команд по запросу.
    ''',
    responses={
        HTTP_200_OK: {
            'model': list[CommentScheme],
            'description': 'Объект получен',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        }
    }
)
@cache(expire=60)
async def get_comments(
        task_id: Annotated[
            str | None,
            Query(
                title='ID Задачи',
                description='Получить комментарии для задачи'
            )
        ],
        session: AsyncSession = Depends(get_db),

) -> JSONResponse:
    crud: CommentCRUD = CommentCRUD(task_id=task_id)
    if obj_list := await crud.get(session):

        response: list[dict] = [
            {
                attr: getattr(obj, attr)
                for attr in CommentScheme.schema().get('properties')
            }
            for obj in obj_list
        ]
        return JSONResponse(
            content=response,
            status_code=HTTP_200_OK,
        )

    else:
        return JSONResponse(
            content=NotFoundScheme().dict(),
            status_code=HTTP_404_NOT_FOUND,
        )
