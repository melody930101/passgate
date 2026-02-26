from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'mysql+pymysql://root:root@localhost:3306/passgate'
    SECRET_KEY: str = 'change-me-in-production'
    JWT_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: list[str] = ['*']
    TIMEZONE: str = 'Asia/Shanghai'

    class Config:
        env_file = '.env'


settings = Settings()
