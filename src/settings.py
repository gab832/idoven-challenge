import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = os.getenv('SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
    algorithm: str = os.getenv('ALGORITHM', 'HS256')
    access_token_expire_minutes: int = int(os.getenv('EXPIRATION_TOKEN_MINUTES', 30))
    api_prefix: str = os.getenv('API_PREFIX', '/api')
    sql_alchemy_database_url: str = os.getenv('DATABASE', 'sqlite:///./sql_app.db')

settings = Settings()
