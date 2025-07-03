import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from src.settings import get_settings

setting = get_settings()
fernet = Fernet(setting.fernet)


def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()


def generate_pkce():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("utf-8")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("utf-8")).digest()
    ).rstrip(b"=").decode("utf-8")
    return verifier, challenge
