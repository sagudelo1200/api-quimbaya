#!/usr/bin/env python3
from os import getenv

import pymysql
pymysql.install_as_MySQLdb()

storage_type = getenv('QUIMBAYA_TYPE_STORAGE')
if not storage_type:
    raise OSError('Missing environment variable with the type of storage')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
elif storage_type == 'fs':
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
else:
    raise ValueError(f'{storage_type} storage type is invalid')

storage.reload()
