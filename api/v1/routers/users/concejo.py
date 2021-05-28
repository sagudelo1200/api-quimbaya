#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends
from models import storage
from models.concejo import Concejo
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/concejo', tags=['Concejo'])


@router.get('/')
async def get_concejo():
    ''' get the list of CONCEJO members '''
    return storage.all(Concejo)


@router.get('/{user_id}/', response_model=schemes.users.User)
async def get_concejo_user(
    user_id: str
) -> schemes.users.User:
    ''' get a CONCEJO member '''
    user = storage.get(Concejo, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[CONCEJO] User {user_id} was not found'
        )
    return user


@router.post('/', response_model=schemes.users.UserInDB)
async def post_concejo_user(
    data: schemes.users.UserForm
):
    ''' '''
    id = data.id or None
    if id and storage.get(Concejo, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'[CONCEJO] There is already a user with the id {id}'
        )

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Concejo(**_dict)
    user.save()
    return user.to_dict()
