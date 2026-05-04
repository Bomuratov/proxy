from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from dotenv import load_dotenv
from pathlib import Path
from typing import Union

BASE_DIR = Path(__file__).parent
print(BASE_DIR)

load_dotenv(dotenv_path=Path(BASE_DIR, ".env"), override=True)

class EskizConfig(BaseModel):
    sms_url: str
    auth_url:str
    email: str
    password: str

class BotConfig(BaseModel):
    chat_id: str
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SET_",
    )
    eskiz: EskizConfig
    bot: BotConfig


settings = Settings()

