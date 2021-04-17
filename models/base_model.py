#!/usr/bin/env python3
''' Contains BaseModel class '''
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
import models
import sqlalchemy

Base = declarative_base()
ftime = '%Y-%m-%dT%H:%M:%S.%f'


class BaseModel():
    '''[The BaseModel class from which future classes will be derived]
    '''
    id = Column(String(30), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs: dict) -> object:
        ''' Initialization of the base model '''
        for key, val in kwargs.items():
            if key != '__class__':
                self.__setattr__(key, val)
        if kwargs.get('created_at'):
            created_at = datetime.strptime(kwargs['created_at'], ftime)
            self.__setattr__('created_at', created_at)
        else:
            self.__setattr__('created_at', datetime.utcnow())
        if kwargs.get('updated_at'):
            updated_at = datetime.strptime(kwargs['updated_at'], ftime)
            self.__setattr__('updated_at', updated_at)
        else:
            self.__setattr__('updated_at', datetime.utcnow())
        if not kwargs.get('id'):
            self.__setattr__('id', str(uuid4()).replace('-', '')[:20])

    def __setattr__(self, attr: str, val: str) -> str:
        ''' Sets the class attributes that are allowed '''
        if attr != '__class__':
            object.__setattr__(self, attr, val)

    def __str__(self) -> str:
        ''' String representation of the class '''
        new_dict = self.__dict__.copy()
        if new_dict.get('password'):
            new_dict['password'] = 'PROTECTED-DATA'

        return f'[{self.__class__.__name__}] ({self.id}) {new_dict}'

    def __repr__(self) -> str:
        ''' Representation of the class '''
        return self.__str__()

    def to_dict(self, show_passwords: bool = False) -> dict:
        ''' Convert an object to its dict representation '''
        new_dict = self.__dict__.copy()
        if 'created_at' in new_dict:
            new_dict['created_at'] = new_dict['created_at'].strftime(ftime)
        if 'updated_at' in new_dict:
            new_dict['updated_at'] = new_dict['updated_at'].strftime(ftime)
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        new_dict['__class__'] = self.__class__.__name__

        if not show_passwords:
            if new_dict.get('password'):
                new_dict['password'] = 'PROTECTED-DATA'

        return new_dict

    def save(self):
        '''[updates the attribute 'updated_at' with the current datetime
        and save the obj]
        '''
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def destroy(self):
        '''[delete the current instance from the storage]
        '''
        models.storage.delete(self)
        models.storage.save()


if __name__ == '__main__':
    pass
