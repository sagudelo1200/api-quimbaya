#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends
from models import storage
from models.sociedad import Sociedad
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/sociedad', tags=['Sociedad'])


@router.get('/')
async def get_sociedad():
    ''' get the list of SOCIEDAD members '''
    return storage.all(Sociedad)


@router.get('/{user_id}/', response_model=schemes.users.User)
async def get_sociedad_user(
    user_id: str
) -> schemes.users.User:
    ''' get a SOCIEDAD member '''
    user = storage.get(Sociedad, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[SOCIEDAD] User {user_id} was not found'
        )
    return user


@router.post('/', response_model=schemes.users.UserInDB)
async def post_sociedad_user(
    data: schemes.users.UserForm
):
    ''' '''
    id = data.id or None
    if id and storage.get(Sociedad, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'[SOCIEDAD] There is already a user with the id {id}'
        )

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Sociedad(**_dict)
    user.save()
    return user.to_dict()
