import psycopg2
from psycopg2 import sql, OperationalError
from psycopg2.extras import DictCursor
from contextlib import contextmanager


class PostgresClient:
    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            database: str,
    ):
        self.conn_params = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "dbname": database,
        }

    @contextmanager
    def get_cursor(self):
        conn = psycopg2.connect(**self.conn_params)
        conn.autocommit = False
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                yield cursor
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute(self, query: str, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())  # Если params=None, подставится ()
            if cursor.description:  # Если запрос возвращает данные (SELECT)
                return cursor.fetchall()

    def table_exists(self, table_name: str) -> bool:
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """
        return self.execute(query, (table_name,))[0][0]

    def get_max_date(self, table_name: str) -> str:
        query = sql.SQL("SELECT MAX(date) FROM {}").format(
            sql.Identifier(table_name)
        )
        result = self.execute(query)
        return result[0][0] if result and result[0][0] else None

    def check_connection(self) -> bool:
        """Проверяет соединение с PostgreSQL. Возвращает True, если успешно."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1;")
                return True
        except OperationalError as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            return False
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return False
