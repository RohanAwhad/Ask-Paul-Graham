from peewee import *

DB = SqliteDatabase('data/tmp.db')
# DB = SqliteDatabase('db.sqlite')

# ==== Models ====

class BaseModel(Model):
    class Meta:
        database = DB

class Article(BaseModel):
    uid = CharField(unique=True)
    title = CharField()
    content = TextField()
    url = CharField()

class Chunk(BaseModel):
    id = AutoField(primary_key=True)
    article = ForeignKeyField(Article, backref='chunks')
    chunk = TextField(unique=True)


if __name__ == '__main__':
    with DB:
        DB.create_tables([Article, Chunk])
        