from peewee import *
from os.path import dirname
import os.path
from datetime import datetime
__author__ = 'zz'

# make sqlite file live in top level
db_dir = dirname(dirname(__file__))
db_name = 'db.sqlite3'


db = SqliteDatabase(os.path.join(db_dir, db_name))



class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_all(cls):
        return cls.select().dicts()

    @classmethod
    def delete_by_id(cls, id):
        q = cls.select().where(cls.id==id)
        if q.exists():
            obj = q.get()
            obj.delete_instance()

    @classmethod
    def create_or_update_data(cls, data):
        id = data.pop('id')
        obj, created = cls.get_or_create(id=id, defaults=data)
        if not created:
            is_success = cls.update(**data).where(cls.id==id).execute()
            return is_success
        else:
            return created


class Tasks(BaseModel):
    url = CharField(max_length=255)
    response_gt = IntegerField()
    create_time = DateTimeField(default=datetime.now())
    max_page = IntegerField()
    is_using = IntegerField(default=1)


class Bookmark(BaseModel):
    link = CharField(max_length=255)
    response_num = IntegerField()
    text = TextField()
    image_path = CharField(max_length=255, null=True)

    
    def has_image(self):
        if self.image_path:
            return True
        else:
            return False


def connect_to_db():
    db.connect()
    db.create_tables([Tasks, Bookmark], True)





