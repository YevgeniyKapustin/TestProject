from sqlalchemy import Column, String

from database import Base


class User(Base):
    access_token: str = Column(String(), nullable=False)
    refresh_token: str = Column(String(), nullable=False)
