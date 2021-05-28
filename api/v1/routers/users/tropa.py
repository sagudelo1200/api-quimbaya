#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends
from models import storage
from models.tropa import Tropa
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/tropa', tags=['Tropa'])


@router.get('/')
async def get_tropa():
    ''' get the list of TROPA members '''
    return storage.all(Tropa)


@router.get('/{user_id}/', response_model=schemes.users.User)
async def get_tropa_user(
    user_id: str
) -> schemes.users.User:
    ''' get a TROPA member '''
    user = storage.get(Tropa, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[TROPA] User {user_id} was not found'
        )
    return user


@router.post('/', response_model=schemes.users.UserInDB)
async def post_clan_user(
    data: schemes.users.UserForm
):
    ''' '''
    id = data.id or None
    if id and storage.get(Tropa, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'[TROPA] There is already a user with the id {id}'
        )

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Tropa(**_dict)
    user.save()
    return user.to_dict()
