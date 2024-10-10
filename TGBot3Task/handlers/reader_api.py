import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

DOTENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "api.env")


class Settings(BaseSettings):
    api_key: SecretStr
    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding="utf-8"
    )


config = Settings()
