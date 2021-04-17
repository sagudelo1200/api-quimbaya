#!/usr/bin/python3
'''
Contains the FileStorage class
'''

from models.user import User
import json
import models
import os

classes = {'User': User}


class FileStorage:
    '''serializes instances to a JSON file & deserializes back to instances'''

    # string - path to the JSON file
    __file_path = 'stored_data.json'
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def __init__(self):
        '''Validate if storage file exists if you don't create it'''
        if not os.path.isfile(self.__file_path):
            with open(self.__file_path, 'w') as f:
                f.write('{}\n')

    def all(self, cls=None):
        '''returns the dictionary __objects'''
        if cls:
            _dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    _dict[key] = value
            return _dict
        return self.__objects

    def new(self, obj):
        '''sets in __objects the obj with key <obj class name>.id'''
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        '''serializes __objects to the JSON file (path: __file_path)'''
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict(
                show_passwords=True
            )
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        '''deserializes the JSON file to __objects'''
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]['__class__']](**jo[key])
        except Exception:
            raise OSError(f'Could not read {self.__file_path} file\n\t{e}')

    def delete(self, obj):
        '''delete obj from __objects if it’s inside'''
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        '''call reload() method for deserializing the JSON file to objects'''
        self.reload()

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

    def count(self, cls=None):
        '''
        counts the number of stored CLS type objects
        '''
        count = 0

        if not cls:
            for _cls in classes.values():
                count += len(models.storage.all(_cls).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
