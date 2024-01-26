from datetime import timedelta
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from authentication.crud import (
    get_user,
    create_access_token,
    create_user,
)
from authentication.schemas import UserCreate, User, Token
from settings import settings
from database import get_db


routers = APIRouter(
    prefix=settings.api_prefix,
    tags=['authentication'],
)


@routers.post(
    '/authentication/user',
    summary='Create new user',
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
def insert_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = create_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The username already exists',
        )
    return user


@routers.post(
    '/authentication/user/login',
    summary='Login user',
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = get_user(
        db,
        form_data.username,
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'email': user.email, 'user_id': user.id, 'scope': user.role},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer')
