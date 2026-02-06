import base64
import hashlib
from cryptography.fernet import Fernet

from app.core.config import settings


def _derive_key() -> bytes:
    digest = hashlib.sha256(settings.secret_key.encode()).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt_value(value: str) -> str:
    fernet = Fernet(_derive_key())
    return fernet.encrypt(value.encode()).decode()


def decrypt_value(value: str) -> str:
    fernet = Fernet(_derive_key())
    return fernet.decrypt(value.encode()).decode()
