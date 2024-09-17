from pydantic import BaseModel


class CommentScheme(BaseModel):
    id: int
    text: str
    task_id: str


class CommentCreateScheme(BaseModel):
    text: str
    task_id: str


class NotFoundScheme(BaseModel):
    """Схема 404 NotFound."""
    message: str = 'NotFound'
    description: str = 'Объект не найден'


class OkScheme(BaseModel):
    """Схема 200 OK."""
    message: str = 'OK'
    description: str = 'Выполнено'


class CreateScheme(BaseModel):
    """Схема 201 Create."""
    message: str = 'Create'
    description: str = 'Создано'


class BadRequestScheme(BaseModel):
    """Схема 400 BadRequest."""
    message: str = 'BadRequest'
    description: str = 'Ошибочный запрос'
