#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends, status
from models import storage
from api.v1 import schemes
from models.engine.authentication import get_current_active_user
from typing import Optional
from models.engine.db_storage import USER_CLASSES

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_users():
    '''  '''
    users = []
    for model in USER_CLASSES:
        _users = storage.all(model)
        for user in _users.values():
            users.append(user)
    return users


@router.get('/{user_id}/', response_model=schemes.users.UserInDB)
async def get_user(
    user_id: str
) -> schemes.users.User:
    '''  '''
    users = []
    for model in USER_CLASSES:
        dict_users = storage.all(model)
        for user in dict_users.values():
            if user.id == user_id:
                return user.to_dict()

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f'User {user_id} was not found'
    )


@router.post('/', response_model=schemes.users.UserInDB)
async def post_user(
    form: schemes.users.UserForm
) -> schemes.users.UserForm:
    '''  '''
    print(form.unit)
    if form.unit not in USER_CLASSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Incorrect \'{form.unit}\' value for unit'
        )
    for cls in USER_CLASSES:
        if storage.get(cls=cls, id=form.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'There is already a user with the id {form.id}'
            )
    for cls in USER_CLASSES:
        if cls == form.unit or cls.__class__.__name__ == form.unit:
            user = USER_CLASSES[cls](**form.__dict__)
            user.save()
            return user.to_dict()
