import os
from datetime import datetime, timedelta
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, computed_field

_ = load_dotenv()

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
    admin_id: str


    @computed_field
    @property
    def jwt_exp(self) -> int:
        return int((datetime.now() + timedelta(minutes=self.jwt_expire_base)).timestamp())


    @computed_field
    @property
    def jwt_refresh_exp(self) -> int:
        return int((datetime.now() + timedelta(minutes=self.jwt_expire_base*100)).timestamp())




_config: Settings | None = None


def instance() -> Settings:
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
            "jwt_expire_base": 30,
            "admin_id": os.getenv('ADMIN_ID')
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
            "jwt_expire_base": 30,
            "admin_id": os.getenv('ADMIN_ID')
        },
    }

    env_config = defaults.get(stage, defaults['dev'])
    settings = Settings(stage=stage, **env_config)

    if settings.use_rich_traceback:
        from rich.traceback import install

        _ = install(show_locals=True)

    _config = settings
    return settings


def get_settings() -> Settings:
    global _config
    if _config is None:
        return instance()
    return _config
