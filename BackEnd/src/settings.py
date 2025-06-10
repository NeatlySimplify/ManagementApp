import os
from datetime import datetime, timedelta
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, computed_field

load_dotenv()

class Settings(BaseModel):
    stage: str = "prod"
    debug: bool = False
    use_rich_traceback: bool = False
    httponly: bool = True
    secure: bool = True
    samesite: Literal["lax", "strict", "none"] = "strict"
    email: EmailStr
    password: str
    secret: str
    session_secret: str
    algorithm: str
    jwt_expire_base: float


    @computed_field
    @property
    def jwt_exp(self) -> int:
        value = int((datetime.now() + timedelta(minutes=self.jwt_expire_base)).timestamp())
        return value


    @computed_field
    @property
    def jwt_refresh_exp(self) -> int:
        value = int((datetime.now() + timedelta(minutes=self.jwt_expire_base*100)).timestamp())
        return value




_config: Settings | None = None


def instance() -> None:
    global _config

    stage = os.getenv('STAGE', 'dev')

    # Default values per environment
    defaults = {
        'dev': {
            'use_rich_traceback': True,
            'secure': False,
            'samesite': "lax",
            "email": os.getenv('EMAIL'),
            "password": os.getenv('PASSWORD'),
            "secret": os.getenv('SECRET'),
            "session_secret": os.getenv('SESSION_SECRET'),
            "algorithm": "HS256",
            "jwt_expire_base": 30
        },
        'prod': {
            'debug': False,
            'use_rich_traceback': False,
            'secure': True,
            'samesite': "strict",
            "email": os.getenv('EMAIL'),
            "password": os.getenv('PASSWORD'),
            "secret": os.getenv('SECRET'),
            "session_secret": os.getenv('SESSION_SECRET'),
            "algorithm": "HS256",
            "jwt_expire_base": 30
        },
    }

    env_config = defaults.get(stage, defaults['dev'])
    settings = Settings(stage=stage, **env_config)

    if settings.use_rich_traceback:
        from rich.traceback import install

        install(show_locals=True)

    _config = settings
    return


def get_settings() -> Settings:
    global _config
    if _config is None:
        instance()
    return _config
