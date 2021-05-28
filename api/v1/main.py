#!/usr/bin/env python3
from api.v1.routers import router
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from api.v1 import schemes
from models.engine.authentication import (
    authenticate_user, create_access_token, get_current_active_user
)
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title='API Quimbaya',
              description='REST API for the administration of Scout groups',
              version='0.1.0',
              )

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*']
)


@app.get('/')
def read_root():
    return {'resourse': app.title, 'status': 'OK', 'version': app.version}


@app.post("/token/", response_model=schemes.token.Token)
async def login_for_access_token(
    request: Request,
):
    exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        json_data = await request.json()
    except Exception:
        raise exeption
    form_data = schemes.users.UserLoginForm(**json_data)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise exeption
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/users/me/", response_model=schemes.users.User)
async def read_users_me(
    current_user: schemes.users.UserInDB = Depends(get_current_active_user)
):
    return current_user
