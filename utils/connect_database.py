from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from decouple import config

db_name = config('DB_NAME')
db_user = config('DB_USER')
db_pass = config('DB_PASS')
db_host = config('DB_HOST')
db_port = config('DB_PORT')


def get_engine():
    url = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url)
    return engine

def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session