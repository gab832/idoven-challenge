from enum import IntEnum

from sqlalchemy import Boolean, Column, Enum, Integer, String

from database import Base


class Role(IntEnum):
    USER = 1
    ADMIN = 2


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Integer, Enum(Role))
