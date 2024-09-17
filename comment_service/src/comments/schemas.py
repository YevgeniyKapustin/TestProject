from pydantic import BaseModel


class CommentScheme(BaseModel):
    id: int
    text: str
    task_id: str


class NotFoundScheme(BaseModel):
    """Схема 404 NotFound."""
    message: str = 'NotFound'
    description: str = 'Объект не найден'
