from sqlalchemy import Table, Column, Integer, String, MetaData, Text, Date
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData

url = "postgresql+psycopg2://kosteniuk:1242@localhost/test_apartament"

engine = create_engine(url)
print(database_exists(engine.url))

meta = MetaData()


apartament = Table(
    'apartament', meta,
    Column("apartament_id", Integer, primary_key=True),
    Column("img_url", String),
    Column("title", String),
    Column("date", Date),
    Column("location", String),
    Column("beds", String),
    Column("description", Text),
    Column("price", String)
)


def create_db():
    if not database_exists(url):
        create_database(url)
        meta.create_all(engine)
