#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from models import storage
from models.clan import Clan
from models.engine.authentication import get_current_active_user
import api.v1.schemes as schemes

router = APIRouter(prefix='/clan', tags=['Clan'])


@router.get('/')
async def get_clan():
    ''' get the list of CLAN members '''
    return storage.all(Clan)


@router.get('/{user_id}/', response_model=schemes.users.UserInDB)
async def get_clan_user(
    user_id: str
) -> schemes.users.UserInDB:
    ''' get a CLAN member '''
    user = storage.get(Clan, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'[CLAN] User {user_id} was not found'
        )
    return user.to_dict()


@router.post('/', response_model=schemes.users.UserInDB)
async def post_clan_user(
    data: schemes.users.UserForm
):
    ''' '''
    id = data.id or None
    _exeption = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=''
    )
    if not id or not data.name or not data.last_name or not data.password:
        _exeption.detail = '[CLAN] Required values are missing'
        raise _exeption
    if storage.get(Clan, id):
        _exeption.detail = f'[CLAN] There is already a user with the id {id}'
        raise _exeption

    _dict = {}
    for k, v in data.__dict__.items():
        _dict[k] = v

    user = Clan(**_dict)
    user.save()
    return user.to_dict()
