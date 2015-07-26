from peewee import *
from os.path import dirname
__author__ = 'zz'

# make sqlite file live in top level
db_path = dirname(dirname(__file__))

db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db

class Tasks(Model):
    url = CharField(max_length=255)
    response_gt = IntegerField()


def connect_to_db():
    db.connect()
    db.create_tables([Tasks], True)



