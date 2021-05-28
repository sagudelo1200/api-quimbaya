#!/usr/bin/env python3
''' User model '''
from models import storage_type
from models.base_model import BaseModel
from sqlalchemy import Column, Boolean, Integer, String, JSON, DateTime, Text
from models.engine.authentication import get_password_hash


class User(BaseModel):
    ''' Gets and handles a user object '''
    if storage_type == 'db':
        address = Column(JSON)
        # full_address, city, neighborhood, street, suite, zipcode, geo
        birthday = Column(String(32))
        disabled = Column(Boolean, default=False)
        email = Column(String(64))
        eps = Column(String(32))
        gender = Column(String(1))  # M, F or X
        hashed_password = Column(String(256), nullable=False)
        header_photo = Column(String(256), default='https://picsum.photos/800')
        id_type = Column(String(16))
        last_name = Column(String(64), nullable=False)
        mobile = Column(String(32))
        name = Column(String(32), nullable=False)
        phone = Column(String(32))
        photo = Column(String(256), default='https://picsum.photos/800')
        rh = Column(String(4))
        status = Column(String(32), default='undefined')
        tutor = Column(JSON)
        # {mother, father or tutor: {full_name, id, phone, email}}

    class Config:
        ''' settings for orm relationships '''
        orm_mode = True

    def __init__(self, **kwargs: dict) -> object:
        ''' instantiate the object '''
        password = kwargs.get('password')
        if password:
            kwargs['hashed_password'] = get_password_hash(password)
            kwargs.pop('password', None)
        super().__init__(**kwargs)
        self.username = self.id
        self.unit = self.__class__.__name__
        if not password and not self.hashed_password:
            self.hashed_password = get_password_hash(self.id)
