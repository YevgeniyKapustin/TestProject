from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфиг приложения."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.POSTGRES_URL: str = self.__get_postgres_dsn()

    TOKEN: str
    TODO_BACKEND_URL: str = 'http://localhost'
    COMMENT_BACKEND_URL: str = 'http://localhost:8040'

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_URL: str | None = None

    def __get_postgres_dsn(self) -> str:
        return (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}/{self.POSTGRES_DB}'
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
