from typing import Optional

from pydantic import BaseModel

from ecg.schemas import ECG


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserBase(BaseModel):
    email: str
    role: Optional[int] = 1


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    ecgs: list[ECG] = []

    class Config:
        from_attributes = True
