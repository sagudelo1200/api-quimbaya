#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends
from models import storage
from models.familia import Familia
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/familia', tags=['Familia'])


@router.get('/')
async def get_familia():
    ''' get the list of FAMILIA members '''
    return storage.all(Familia)


@router.get('/{user_id}/', response_model=schemes.users.User)
async def get_familia_user(
    user_id: str
) -> schemes.users.User:
    ''' get a FAMILIA member '''
    user = storage.get(Familia, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[FAMILIA] User {user_id} was not found'
        )
    return user


@router.post('/', response_model=schemes.users.UserInDB)
async def post_familia_user(
    data: schemes.users.UserForm
):
    ''' '''
    print(f'\n\n{data}\n\n')
    id = data.id or None
    if id and storage.get(Familia, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'[FAMILIA] There is already a user with the id {id}'
        )

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Familia(**_dict)
    user.save()
    return user.to_dict()
