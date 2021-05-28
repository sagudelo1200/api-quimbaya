#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends
from models import storage
from models.jefatura import Jefatura
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/jefatura', tags=['Jefatura'])


@router.get('/')
async def get_jefatura():
    ''' get the list of JEFATURA members '''
    return storage.all(Jefatura)


@router.get('/{user_id}/', response_model=schemes.users.User)
async def get_jefatura_user(
    user_id: str
) -> schemes.users.User:
    ''' get a JEFATURA member '''
    user = storage.get(Jefatura, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[JEFATURA] User {user_id} was not found'
        )
    return user


@router.post('/', response_model=schemes.users.UserInDB)
async def post_jefatura_user(
    data: schemes.users.UserForm
):
    ''' '''
    id = data.id or None
    if id and storage.get(Jefatura, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'[JEFATURA] There is already a user with the id {id}'
        )

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Jefatura(**_dict)
    user.save()
    return user.to_dict()
