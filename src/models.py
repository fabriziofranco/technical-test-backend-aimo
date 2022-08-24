from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField,  ForeignKeyField
import datetime

db = SqliteDatabase("tech_test_notes.db")

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=20, unique=True, null=False)
    password = CharField(max_length=20, null=False)


class Note(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=200, null=False)
    creation_date = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User)