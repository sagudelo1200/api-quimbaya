#!/usr/bin/env python3
from .user import User
from pydantic import BaseModel
from typing import Optional


class LoginUser(BaseModel):
    id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str


class UserLoginForm(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: Optional[str]
