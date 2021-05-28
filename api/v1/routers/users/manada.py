#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends
from models import storage
from models.manada import Manada
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/manada', tags=['Manada'])


@router.get('/')
async def get_manada():
    ''' get the list of MANADA members '''
    return storage.all(Manada)


@router.get('/{user_id}/', response_model=schemes.users.User)
async def get_manada_user(
    user_id: str
) -> schemes.users.User:
    ''' get a MANADA member '''
    user = storage.get(Manada, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[MANADA] User {user_id} was not found'
        )
    return user


@router.post('/', response_model=schemes.users.UserInDB)
async def post_manada_user(
    data: schemes.users.UserForm
):
    ''' '''
    id = data.id or None
    if id and storage.get(Manada, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'[MANADA] There is already a user with the id {id}'
        )

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Manada(**_dict)
    user.save()
    return user.to_dict()
