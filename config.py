from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings(BaseSettings):
    app_env: str
    allow_origins: str
    api_gateway_token: str
    secret_key: str
    algorithm: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int = 5432
    database_name: str
    google_maps_api_key: str


    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.database_user}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )

    class Config:
        env_file = ".env"

settings = Settings()