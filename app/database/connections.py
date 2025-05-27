import psycopg2, sys
from config import config

# Напишем декоратор для подключения к базе данных PostgreSQL
def db_connect(func):
    def wraper(*args, **kwargs):
        try:
            with psycopg2.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                dbname=config.DB_NAME
            ) as conn:
                with conn.cursor() as cursor:
                    return func(cursor, *args, **kwargs)
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            sys.exit(1)
    return wraper


