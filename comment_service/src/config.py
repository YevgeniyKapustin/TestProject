from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфиг приложения."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.POSTGRES_URL: str = self.__get_postgres_dsn()

    # Postgres
    DEFAULT_USER: str
    DEFAULT_PASSWORD: str
    DEFAULT_HOST: str
    DEFAULT_PORT: str
    DEFAULT_NAME: str
    POSTGRES_URL: str | None = None

    # CORS
    ALLOWED_HOSTS: list[str]

    def __get_postgres_dsn(self) -> str:
        return (
            f'postgresql://{self.DEFAULT_USER}:{self.DEFAULT_PASSWORD}@'
            f'{self.DEFAULT_HOST}/{self.DEFAULT_NAME}'
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
