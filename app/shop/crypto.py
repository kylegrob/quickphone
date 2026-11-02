"""Encryption of the optional device passcode (owner, Oct 23 #7)."""
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


def _fernet():
    key = settings.PASSCODE_KEY
    if not key:
        key = base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest())
    return Fernet(key)


def encrypt_passcode(plain):
    return _fernet().encrypt(plain.encode()).decode() if plain else None


def decrypt_passcode(token):
    if not token:
        return ""
    try:
        return _fernet().decrypt(token.encode()).decode()
    except InvalidToken:
        return "(cannot be decrypted with the current key)"
