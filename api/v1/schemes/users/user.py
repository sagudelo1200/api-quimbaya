#!/usr/bin/env python3
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User(BaseModel):
    address: Optional[dict] = {
        'full_address': '',
        'city': '',
        'neighborhood': '',
        'state': '',
        'zip': '',
        'geo': {
            'lat': '',
            'long': '',
        },
    }
    birthday: Optional[str] = ''
    disabled: bool = False
    email: Optional[str] = ''
    eps: Optional[str] = ''
    gender: Optional[str] = ''
    header_photo: Optional[str] = 'https://picsum.photos/800'
    id_type: Optional[str] = ''
    id: Optional[str] = ''
    last_name: str  # Required
    mobile: Optional[str] = ''
    name: str  # Required
    phone: Optional[str] = ''
    photo: Optional[str] = 'https://picsum.photos/800'
    rh: Optional[str] = ''
    status: Optional[str] = 'active'
    tutor: Optional[dict] = {
        'id': '',
        'full_name': '',
        'mobile': '',
        'email': '',
    }
    username: Optional[str] = ''
    unit: Optional[str] = ''


class UserForm(User):
    password: str  # Required
