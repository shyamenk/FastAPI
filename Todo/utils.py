from fastapi import HTTPException
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes="bcrypt", depreciated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def http_notfound_exception(message: str):
    return HTTPException(status_code=404, detail=f"{message} not found!")
