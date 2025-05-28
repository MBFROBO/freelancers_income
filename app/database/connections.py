import warnings
import psycopg2, sys
from config import config


class Database:
    """
    Класс для работы с базой данных PostgreSQL.
    Использует декоратор для подключения к базе данных.
    """
    @staticmethod    
    def db_connect(func):
        async def wrapper(*args, **kwargs):
            with warnings.catch_warnings():
                conn = psycopg2.connect(
                    host=config.DB_HOST,
                    database=config.DB_NAME,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    port=config.DB_PORT
                )

                try:
                    result = await func(*args, **kwargs, conn=conn)
                    conn.commit() 
                    return result
                except Exception as e:
                    conn.rollback()
                    raise e
                finally:
                    conn.close()
        return wrapper

