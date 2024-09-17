from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST

from comments.schemas import CommentScheme, NotFoundScheme, OkScheme, \
    CreateScheme, CommentCreateScheme, BadRequestScheme
from comments.services import CommentCRUD
from comments.utils import check_exist_task
from database import get_db

router = APIRouter(
    prefix='/api/v1',
    tags=['Комментарии'],
)


@router.get(
    '/comments',
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


@router.post(
    '/comments',
    name='Создает комментарий',
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект уже существует',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Объект создан',
        }
    }
)
async def create_comment(
        comment: CommentCreateScheme,

        session: AsyncSession = Depends(get_db),

) -> JSONResponse:
    if check_exist_task(comment.task_id):
        return JSONResponse(
            content=BadRequestScheme().dict(),
            status_code=HTTP_400_BAD_REQUEST,
        )

    obj: CommentCRUD = CommentCRUD(
        task_id=comment.task_id,
        text=comment.text,
    )

    if await obj.get(session):
        return JSONResponse(
            content=OkScheme().dict(),
            status_code=HTTP_200_OK,
        )

    else:
        await obj.create(session)
        await session.commit()
        return JSONResponse(
            content=CreateScheme().dict(),
            status_code=HTTP_201_CREATED,
        )


@router.put(
    '/comment/{id}',
    name='Изменяет комментарий',
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект изменен',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Объект создан',
        },
        HTTP_400_BAD_REQUEST: {
            'model': BadRequestScheme,
            'description': 'Конечный объект уже существует'
        },
    }
)
async def update_comment(
        comment_id: Annotated[
            str | None,
            Query(
                title='ID комментария',
                description='Изменить комментарий'
            )
        ],
        new_comment: CommentCreateScheme,

        session: AsyncSession = Depends(get_db),

) -> JSONResponse:
    if check_exist_task(new_comment.task_id):
        return JSONResponse(
            content=BadRequestScheme().dict(),
            status_code=HTTP_400_BAD_REQUEST,
        )
    original_obj = CommentCRUD(id_=comment_id)
    new_obj: CommentCRUD = CommentCRUD(
        task_id=new_comment.task_id,
        text=new_comment.text,
    )
    data_for_update = new_comment.dict()
    original_obj_orm = await original_obj.get(session)
    new_obj_orm = await new_obj.get(session)

    if original_obj_orm:

        if not new_obj_orm:

            if original_obj_orm == new_obj_orm:
                await original_obj.create(session)
                await session.commit()
                return JSONResponse(
                    content=CreateScheme().dict(),
                    status_code=HTTP_201_CREATED,
                )

            else:
                await original_obj.update(data_for_update, session)
                await session.commit()
                return JSONResponse(
                    content=OkScheme().dict(),
                    status_code=HTTP_200_OK,
                )
        else:
            return JSONResponse(
                content=BadRequestScheme().dict(),
                status_code=HTTP_400_BAD_REQUEST,
            )
    else:
        return JSONResponse(
            content=NotFoundScheme().dict(),
            status_code=HTTP_404_NOT_FOUND,
        )


@router.delete(
    '/comments',
    name='Удаляет комментарий',
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект удален',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        },
    }
)
async def delete_comment(
        comment_id: int,

        session: AsyncSession = Depends(get_db),

) -> JSONResponse:
    obj: CommentCRUD = CommentCRUD(comment_id)
    if await obj.get(session):
        await obj.delete(session)
        await session.commit()
        return JSONResponse(
            content=OkScheme().dict(),
            status_code=HTTP_200_OK,
        )

    else:
        return JSONResponse(
            content=NotFoundScheme().dict(),
            status_code=HTTP_404_NOT_FOUND,
        )
