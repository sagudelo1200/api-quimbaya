#!/usr/bin/env python3
'''
QUIMBAYA_MYSQL_HOST='localhost' QUIMBAYA_MYSQL_USER='agudelo' QUIMBAYA_MYSQL_PWD='*FLDSmdfr*1200*' QUIMBAYA_MYSQL_DB='quimbaya' QUIMBAYA_TYPE_STORAGE='db' QUIMBAYA_SECRET_KEY='agudelo420a8bb13dc3bbc18768c7433db3c43b39e399e3b6ef1326bd4fe564e' QUIMBAYA_ENV='test' python test.py
'''
from models.familia import Familia
from models.clan import Clan
from models.manada import Manada
from models.tropa import Tropa
from models import storage
from time import sleep
from models.engine.db_storage import CLASSES


for cls in CLASSES:
    user = CLASSES[cls](
        status='active',
        name='Jane',
        password='1200',
        header_photo=None,
        last_name='Doe',
        id_type=None,
        gender='F',
        birthday=None,
        eps=None,
        rh='AB+',
        phone='847-361-8609',
        mobile='224-612-9414',
        email='john@doe.com',
        tutor={
            'full_name': 'TUTOR NAME',
            'phone': 'TUTOR PHONE',
            'email': 'TUTOR EMAIL'
        },
        address={
            'full_address': 'Hickory Hills, Illinois(IL), 60457',
            'city': 'Hickory Hills',
            'neighborhood': '2006 Victoria Street',
            'zip': '60457',
            'geo': {
                'lat': '',
                'long': ''
            }
        }
    )
    user.save()
