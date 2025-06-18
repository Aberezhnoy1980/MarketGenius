import csv
from io import StringIO
from datetime import datetime
from typing import List, Dict
from tqdm import tqdm
import logging
from psycopg2 import sql

from src.S3ToPostgresETL.cnSanitizer import sanitize_column_name
from src.clients.db_client.src.simplest_pg_client.pg_client import PostgresClient
from src.clients.s3_client.src.simplest_async_s3client.s3client import S3Client

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('etl_process.log')
    ]
)
logger = logging.getLogger(__name__)


class S3ToPostgresETL:
    """
    Класс для выполнения ETL процесса из S3 в PostgreSQL.

    Attributes:
        s3_client (S3Client): Клиент для работы с S3
        pg_client (PostgresClient): Клиент для работы с PostgreSQL
    """

    def __init__(self, s3_client: S3Client, pg_client: PostgresClient):
        self.s3_client = s3_client
        self.pg_client = pg_client

    async def process_bucket(self, bucket_name: str):
        """
        Обрабатывает все CSV файлы в указанном бакете S3.

        Args:
            bucket_name (str): Название бакета в S3
        """
        try:
            logger.info(f"Начало обработки бакета {bucket_name}")
            objects = await self.s3_client.get_object_list(bucket_name)
            csv_files = [obj for obj in objects if obj["Key"].endswith("_final.csv")]

            if not csv_files:
                logger.warning(f"В бакете {bucket_name} не найдено CSV файлов")
                return

            logger.info(f"Найдено {len(csv_files)} CSV файлов для обработки")

            # Обрабатываем файлы с прогресс-баром
            for obj in tqdm(csv_files, desc="Обработка CSV файлов"):
                try:
                    # Извлекаем тикер из названия файла (пример: SBER_final.csv -> sber)
                    ticker = obj["Key"].split('_')[0].lower()
                    await self.process_file(bucket_name, obj["Key"], ticker)
                except Exception as e:
                    logger.error(f"Ошибка при обработке файла {obj['Key']}: {str(e)}")

        except Exception as e:
            logger.error(f"Ошибка при обработке бакета {bucket_name}: {str(e)}")
            raise

    async def process_file(self, bucket_name: str, file_key: str, table_name: str):
        """
        Обрабатывает один CSV файл из S3 и загружает данные в PostgreSQL.

        Args:
            bucket_name (str): Название бакета в S3
            file_key (str): Ключ файла в S3
            table_name (str): Название таблицы в PostgreSQL (тикер в нижнем регистре)
        """
        try:
            logger.info(f"Начало обработки файла {file_key} в таблицу {table_name}")

            # Загружаем CSV файл
            csv_content = await self.download_csv(bucket_name, file_key)
            reader = csv.DictReader(StringIO(csv_content))

            if not reader.fieldnames:
                logger.warning(f"Файл {file_key} пуст или некорректен")
                return

            # Очищаем названия колонок
            sanitized_columns = [sanitize_column_name(col) for col in reader.fieldnames]

            # Проверяем обязательные колонки
            if 'date' not in [col.lower() for col in sanitized_columns]:
                raise ValueError(f"В файле {file_key} отсутствует колонка 'date'")

            # Создаем таблицу если ее нет
            if not self.pg_client.table_exists(table_name):
                self.create_table(table_name, sanitized_columns)
                max_date = None
                logger.info(f"Создана новая таблица {table_name}")
            else:
                max_date = self.pg_client.get_max_date(table_name)
                logger.info(f"Таблица {table_name} существует, максимальная дата: {max_date}")

            # Подготавливаем данные для вставки
            rows_to_insert = []
            for row in reader:
                try:
                    row_date = datetime.strptime(row['date'], "%Y-%m-%d").date()

                    # Если таблица пуста или дата новее максимальной
                    if max_date is None or row_date > max_date:
                        # Очищаем значения в строке
                        clean_row = {}
                        for col, value in row.items():
                            clean_col = sanitize_column_name(col)
                            if clean_col == 'date':
                                clean_row[clean_col] = value
                            elif clean_col == sanitize_column_name(reader.fieldnames[1]):  # Вторая колонка - тикер
                                clean_row[clean_col] = str(value)
                            else:  # Все остальные колонки - числа
                                try:
                                    clean_row[clean_col] = float(value) if value else None
                                except (ValueError, TypeError):
                                    clean_row[clean_col] = None

                        rows_to_insert.append(clean_row)
                except Exception as e:
                    logger.warning(f"Ошибка при обработке строки: {str(e)}")
                    continue

            # Вставляем данные если есть что вставлять
            if rows_to_insert:
                self.insert_data(table_name, sanitized_columns, rows_to_insert)
                logger.info(f"Добавлено {len(rows_to_insert)} записей в таблицу {table_name}")
            else:
                logger.info(f"Нет новых данных для таблицы {table_name}")

        except Exception as e:
            logger.error(f"Ошибка при обработке файла {file_key}: {str(e)}")
            raise

    async def download_csv(self, bucket_name: str, file_key: str) -> str:
        """
        Загружает CSV файл из S3.

        Args:
            bucket_name (str): Название бакета в S3
            file_key (str): Ключ файла в S3

        Returns:
            str: Содержимое CSV файла в виде строки
        """
        async with self.s3_client.get_client() as client:
            response = await client.get_object(Bucket=bucket_name, Key=file_key)
            async with response["Body"] as stream:
                return (await stream.read()).decode("utf-8")

    def create_table(self, table_name: str, columns: List[str]):
        """
        Создает таблицу в PostgreSQL с указанными колонками.

        Args:
            table_name (str): Название таблицы
            columns (List[str]): Список колонок
        """
        # Определяем типы колонок
        column_defs = []
        for i, col in enumerate(columns):
            if col == 'date':
                col_type = 'DATE'
            elif i == 1:  # Вторая колонка - тикер
                col_type = 'TEXT'
            else:
                col_type = 'FLOAT'

            column_defs.append(sql.SQL("{} {}").format(
                sql.Identifier(col),
                sql.SQL(col_type)
            ))

        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(column_defs)
        )
        self.pg_client.execute(query)

    def insert_data(self, table_name: str, columns: List[str], rows: List[Dict]):
        """
        Вставляет данные в таблицу PostgreSQL.

        Args:
            table_name (str): Название таблицы
            columns (List[str]): Список колонок
            rows (List[Dict]): Список строк для вставки
        """
        # Подготавливаем SQL запрос
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join([sql.Placeholder()] * len(columns))
        )

        # Подготавливаем данные для вставки
        values = []
        for row in rows:
            values.append([row.get(col) for col in columns])

        # Выполняем массовую вставку
        with self.pg_client.get_cursor() as cursor:
            cursor.executemany(query, values)
