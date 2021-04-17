#!/usr/bin/env python3
from models.base_model import Base
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import models
import sqlalchemy

classes = {'User': User}


class DBStorage:
    '''[engine that interacts with the database]
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''[instantiate DB Storage object]
        '''
        user = getenv('QUIMBAYA_MYSQL_USER')
        pwd = getenv('QUIMBAYA_MYSQL_PWD')
        host = getenv('QUIMBAYA_MYSQL_HOST')
        db = getenv('QUIMBAYA_MYSQL_DB')
        env = getenv('QUIMBAYA_ENV')

        if not user or not pwd or not host or not db:
            raise OSError('Missing environment variables for the database')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''[query on the current database session]
        '''
        _dict = {}
        for clss in classes:
            if not cls or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    _dict[key] = obj
        return (_dict)

    def close(self):
        '''call remove() method on the private session attribute'''
        self.__session.remove()

    def get(self, cls, id):
        '''
        Returns the object based on the class name and its ID, or
        None if not found
        '''
        if cls not in classes and cls not in classes.values():
            return None

        for value in models.storage.all(cls).values():
            if (value.id == id):
                return value

        return None

    def new(self, obj):
        '''[add the object to the current database session]
        '''
        self.__session.add(obj)

    def save(self):
        '''[commit all changes of the current database session]
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''[delete from the current database session obj if not None]
        '''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''[reloads data from the database]
        '''
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess_factory)

    def close(self):
        '''[call remove() method on the private session attribute]
        '''
        self.__session.remove()

    def count(self, cls=None):
        '''[count the number of objects stored in db]
        '''
        count = 0
        if cls:
            count = len(models.storage.all(cls).values())
        else:
            for clss in classes:
                count += len(models.storage.all(clss).values())
        return count
