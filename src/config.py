from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent / '.env'


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_prefix='db_', extra='ignore')

    user: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TITLE: str
    PROJECT_VERSION: str
    PROJECT_DESCRIPTION: str
    DEBUG: str

    @property
    def debug(self) -> bool:
        return self.DEBUG == 'TRUE'


db_settings = DBSettings()
settings = Settings()
