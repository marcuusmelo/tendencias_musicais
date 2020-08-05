import sqlite3
import psycopg2
from sqlalchemy import create_engine

from credentials import DB_USER, DB_PASSWORD

def get_db_connection():
    conn = sqlite3.connect('/Users/marcusmelo/Desktop/projeto_m4_gh/tendencias_musicais_web/db.sqlite3')
    conn.text_factory = str

    return conn


def get_postgres_db_conn():
    conn = psycopg2.connect(
        database='d8qa6a84s43m9m',
        user=DB_USER,
        password=DB_PASSWORD,
        host='ec2-52-204-20-42.compute-1.amazonaws.com',
        port='5432'
    )

    return conn

def get_postgress_engine():
    engine_str = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER,
        DB_PASSWORD,
        'ec2-52-204-20-42.compute-1.amazonaws.com',
        '5432',
        'd8qa6a84s43m9m'
    )
    engine = create_engine(engine_str)

    return engine
