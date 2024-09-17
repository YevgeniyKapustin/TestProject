"""Сбор метаданных и создание сессии"""
from typing import Generator

from sqlalchemy import Column, Integer, create_engine, Engine

from sqlalchemy.orm import as_declarative, declared_attr, Mapped, sessionmaker, \
    Session
from sqlalchemy.pool import NullPool

from config import settings


@as_declarative()
class Base:
    __name__: str
    id: Mapped[int] = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


engine: Engine = create_engine(
    settings.POSTGRES_URL, poolclass=NullPool
)
session_maker = sessionmaker(engine, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    session: Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine
    )()

    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        raise
    finally:
        session.close()
