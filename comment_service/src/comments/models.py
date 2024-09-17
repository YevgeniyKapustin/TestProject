from sqlalchemy import Column, String

from database import Base


class Comment(Base):
    text: str = Column(String(), nullable=False)
    task_id: str = Column(String(), nullable=False)
