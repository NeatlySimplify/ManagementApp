import os
from datetime import datetime, timedelta
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, computed_field

_ = load_dotenv()

class Settings(BaseModel):
    stage: str = "prod"
    debug: bool = False
    use_rich_traceback: bool = False
    httponly: bool = True
    secure: bool = True
    samesite: Literal["lax", "strict", "none"] = "strict"
    secret: str
    algorithm: str
    jwt_expire_base: float
    gel_url: str = "https://test--neatlysimplified.c-05.i.aws.edgedb.cloud:5656/branch/main/ext/auth/"
    fernet: str
    token_expiration: int = 30 # in days


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
            "secret": os.getenv('SECRET'),
            "algorithm": "HS256",
            "jwt_expire_base": 30,
            "fernet": os.getenv('FERNET')
        },
        'prod': {
            'debug': False,
            'use_rich_traceback': False,
            'secure': True,
            'samesite': "strict",
            "secret": os.getenv('SECRET'),
            "algorithm": "HS256",
            "jwt_expire_base": 30,
            "fernet": os.getenv('FERNET')
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
