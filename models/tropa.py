#!/usr/bin/env python3
''' [TROPA] User model '''
from models.user import User
from models.base_model import Base


class Tropa(User, Base):
    ''' Gets and handles a user object '''
    __tablename__ = 'tropa'

    def __init__(self, **kwargs: dict) -> object:
        ''' instantiate the object '''
        super().__init__(**kwargs)
