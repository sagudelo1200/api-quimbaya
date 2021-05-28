#!/usr/bin/env python3
''' contains the authentication engine '''
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import os
import models

from api.v1 import schemes

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv('QUIMBAYA_SECRET_KEY')
if not SECRET_KEY:
    raise OSError('Missing environment variable with the SECRET KEY')
ALGORITHM = 'HS256'


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token/')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    users = models.storage.all()
    for user in users.values():
        if user.id == username:
            return schemes.users.LoginUser(**user)


def authenticate_user(username: str, password: str):
    users = models.storage.all()
    if not users:
        return False
    user = None
    for _user in users.values():
        if _user.id == username:
            user = _user
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_100_CONTINUE,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = schemes.token.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    users = models.storage.all()
    if not users:
        raise credentials_exception
    for user in users:
        if user.id == token_data.username:
            return user
    raise credentials_exception


async def get_current_active_user(
    current_user: schemes.users.LoginUser = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    current_user.username = current_user.id
    return current_user.to_dict()
