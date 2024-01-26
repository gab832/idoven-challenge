from jose import jwt
from passlib.context import CryptContext

from settings import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def decode_jwt(token):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
