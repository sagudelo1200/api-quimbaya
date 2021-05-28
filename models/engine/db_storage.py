#!/usr/bin/env python3
from models.base_model import Base
from models.clan import Clan
from models.concejo import Concejo
from models.familia import Familia
from models.jefatura import Jefatura
from models.manada import Manada
from models.sociedad import Sociedad
from models.tropa import Tropa
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import scoped_session, sessionmaker
import models
import sqlalchemy

USER_CLASSES = {
    'Familia': Familia, 'Manada': Manada,
    'Tropa': Tropa, 'Sociedad': Sociedad, 'Clan': Clan,
    'Jefatura': Jefatura, 'Concejo': Concejo
}

CLASSES = dict(**USER_CLASSES)


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
        for clss in CLASSES:
            model = CLASSES[clss]
            if not cls or cls is model or cls is clss:
                objs = self.__session.query(model).all()
                for obj in objs:
                    class_name = obj.__class__.__name__
                    if class_name in USER_CLASSES:
                        obj.username = obj.id
                        obj.unit = class_name
                        obj.full_name = f'{obj.name} {obj.last_name}'
                    key = f'{class_name}.{obj.id}'
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
        if cls not in CLASSES and cls not in CLASSES.values():
            return None
        objs = models.storage.all(cls)
        for obj in objs.values():
            if obj.id == id:
                if cls in USER_CLASSES or cls in USER_CLASSES.values():
                    obj.username = id
                    obj.unit = obj.__class__.__name__
                    obj.full_name = obj.name + ' ' + obj.last_name
                return obj
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
            count = len(models.storage.all(cls))
        else:
            for clss in CLASSES:
                count += len(models.storage.all(clss))
        return count
