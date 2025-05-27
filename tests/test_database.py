from config import config
import psycopg2

def test_connection_creds():
    try:
        with psycopg2.connect(
                    host=config.DB_HOST,
                    port=config.DB_PORT,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    dbname=config.DB_NAME
                ) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT 1;")
                        result = cursor.fetchone()
                        assert result[0] == 1
    except psycopg2.Error as e:
        print(f"Ошибка соединения: {e}")
        assert False, f"Ошибка соединения: {e}"
    except Exception as e:
        print(f"Ошибка: {e}")
        assert False, f"Ошибка: {e}"
    else:
        print("Пропущен.")