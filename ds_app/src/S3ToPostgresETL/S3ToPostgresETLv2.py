import csv
import re
from io import StringIO
from datetime import datetime
from typing import List, Dict, Tuple
from tqdm import tqdm
import logging
from psycopg2 import sql

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

COLUMNS_TO_RENAME = [
    ('blog_score', True),  # (pattern, remove_all_prefixes)
    ('blog_score_roll_avg_5', True),
    ('blog_score_roll_avg_15', True),
    ('blog_score_roll_avg_30', True),
    ('news_score', True),
    ('news_score_roll_avg_5', True),
    ('news_score_roll_avg_15', True),
    ('news_score_roll_avg_30', True)
]


def sanitize_column_name(name: str, columns_to_rename: List[Tuple], need_check: bool = True) -> str:
    """
    Очищает название колонки от недопустимых символов для PostgreSQL.

    Args:
        need_check: Флаг для обработки специальных случаев
        columns_to_rename: поля таблицы с недопустимыми символами
        name (str): Исходное название колонки

    Returns:
        str: Очищенное название колонки, пригодное для использования в PostgreSQL
    """
    original_name = name
    name = name.strip().lower()

    # Обрабатываем специальные случаи
    if (need_check):
        if name.startswith('weightedindices_'):
            prefix = 'weightedindices_'
            rest = name[len(prefix):]

            # Обрабатываем специальные случаи после префикса
            for pattern, _ in columns_to_rename:
                if rest == pattern:
                    name = f'{prefix}{pattern}'
                    break
        else:
            # Обрабатываем специальные случаи (удаляем префикс тикера)
            for pattern, _ in columns_to_rename:
                if name.endswith(f'_{pattern}'):
                    name = pattern
                    break

    # Стандартная очистка
    invalid_chars = ['%', ' ', '-', '(', ')', '/', '\\', '?', '!']
    for char in invalid_chars:
        name = name.replace(char, '_')

    name = re.sub('_+', '_', name).strip('_')

    if name and name[0].isdigit():
        name = f'col_{name}'

    if not name:
        logger.warning(f"Пустое название колонки после очистки: {original_name}")
        return None

    if original_name != name:
        logger.debug(f"Переименование колонки: {original_name} → {name}")

    return name


class S3ToPostgresETL:
    """
    Класс для выполнения ETL процесса из S3 в PostgreSQL с использованием единой таблицы.
    Все данные хранятся в таблице securities_data с составным ключом (ticker, date).
    """

    def __init__(self, s3_client: S3Client, pg_client: PostgresClient, table_name: str, need_spec_check: bool = True):
        self.s3_client = s3_client
        self.pg_client = pg_client
        self.main_table = table_name
        self.need_spec_check = need_spec_check

        # Инициализация основной таблицы при создании ETL
        self.initialize_main_table()

    def initialize_main_table(self):
        """Проверяет существование основной таблицы и создает ее при необходимости."""
        if not self.pg_client.table_exists(self.main_table):
            self.create_main_table()
            logger.info(f"Создана новая таблица {self.main_table}")
        else:
            logger.info(f"Таблица {self.main_table} уже существует")

    def create_main_table(self):
        """Создает основную таблицу для хранения всех данных."""
        table_id = sql.Identifier(self.main_table)
        index_name = sql.Identifier(f"idx_{self.main_table}_date")

        query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {table} (
            secid TEXT NOT NULL,
            date DATE NOT NULL,
            PRIMARY KEY (secid, date)
        );
        CREATE INDEX IF NOT EXISTS {index} ON {table} (date);
        """).format(
            table=table_id,
            index=index_name
        )

        self.pg_client.execute(query)

        # Кластеризуем таблицу после создания
        self.pg_client.execute(f"CLUSTER {self.main_table} USING {self.main_table}_pkey")

    async def process_bucket(self, bucket_name: str):
        """
        Обрабатывает все CSV файлы в указанном бакете S3.
        """
        try:
            logger.info(f"Начало обработки бакета {bucket_name}")
            objects = await self.s3_client.get_object_list(bucket_name)
            csv_files = [obj for obj in objects if obj["Key"].endswith("_final.csv")]

            if not csv_files:
                logger.warning(f"В бакете {bucket_name} не найдено CSV файлов")
                return

            logger.info(f"Найдено {len(csv_files)} CSV файлов для обработки")

            for obj in tqdm(csv_files, desc="Обработка CSV файлов"):
                try:
                    ticker = obj["Key"].split('_')[0].lower()
                    await self.process_file(bucket_name, obj["Key"], ticker)
                except Exception as e:
                    logger.error(f"Ошибка при обработке файла {obj['Key']}: {str(e)}")

        except Exception as e:
            logger.error(f"Ошибка при обработке бакета {bucket_name}: {str(e)}")
            raise

    async def process_file(self, bucket_name: str, file_key: str, ticker: str):
        """
        Обрабатывает один CSV файл из S3 и загружает данные в основную таблицу.
        """
        try:
            logger.info(f"Обработка файла {file_key} для тикера {ticker}")

            csv_content = await self.download_csv(bucket_name, file_key)
            reader = csv.DictReader(StringIO(csv_content))

            if not reader.fieldnames:
                logger.warning(f"Файл {file_key} пуст или некорректен")
                return

            # Очищаем названия колонок
            sanitized_columns = [sanitize_column_name(col, COLUMNS_TO_RENAME, need_check=self.need_spec_check) for col
                                 in reader.fieldnames]

            # Проверяем обязательные колонки
            # if 'date' not in [col.lower() for col in sanitized_columns]:
            #     raise ValueError(f"В файле {file_key} отсутствует колонка 'date'")
            #
            # if 'secid' not in [col.lower() for col in sanitized_columns]:
            #     raise ValueError(f"В файле {file_key} отсутствует колонка 'secid'")

            # Добавляем новые колонки в таблицу если они появились
            self.add_missing_columns(sanitized_columns)

            # Получаем максимальную дату для этого тикера
            max_date = self.get_max_date_for_ticker(ticker)

            # Подготавливаем данные для вставки
            rows_to_insert = []
            for row in reader:
                try:
                    row_date = datetime.strptime(row['date'], "%Y-%m-%d").date()

                    if max_date is None or row_date > max_date:
                        clean_row = {'secid': ticker}
                        for col, value in row.items():
                            clean_col = sanitize_column_name(col, COLUMNS_TO_RENAME, need_check=self.need_spec_check)
                            if clean_col == 'secid':
                                clean_row[clean_col] = value
                            elif clean_col == 'date':
                                clean_row[clean_col] = value
                            else:
                                try:
                                    clean_row[clean_col] = float(value) if value else None
                                except (ValueError, TypeError):
                                    clean_row[clean_col] = 'test'

                        rows_to_insert.append(clean_row)
                except Exception as e:
                    logger.warning(f"Ошибка при обработке строки: {str(e)}")
                    continue

            # Вставляем данные если есть что вставлять
            if rows_to_insert:
                self.insert_data(sanitized_columns, rows_to_insert)
                logger.info(f"Добавлено {len(rows_to_insert)} записей для тикера {ticker}")

                # Периодическая кластеризация (например, после каждых 10 файлов)
                # if len(rows_to_insert) > 1000:
                #     self.pg_client.execute(f"CLUSTER {self.main_table} USING {self.main_table}_pkey")
            else:
                logger.info(f"Нет новых данных для тикера {ticker}")

        except Exception as e:
            logger.error(f"Ошибка при обработке файла {file_key}: {str(e)}")
            raise

    def add_missing_columns(self, columns: List[str]):
        """
        Добавляет новые колонки в основную таблицу если они появились в файле.
        """
        existing_columns = self.get_table_columns()

        for col in columns:
            if col.lower() not in ['secid', 'date'] and col not in existing_columns:
                col_type = 'FLOAT'  # Все показатели кроме даты и тикера храним как FLOAT
                query = sql.SQL("ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} {}").format(
                    sql.Identifier(self.main_table),
                    sql.Identifier(col),
                    sql.SQL(col_type)
                )
                self.pg_client.execute(query)
                logger.info(f"Добавлена новая колонка {col} в таблицу {self.main_table}")

    def get_table_columns(self) -> List[str]:
        """
        Возвращает список колонок в основной таблице.
        """
        query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = %s
        """
        return [row[0] for row in self.pg_client.execute(query, (self.main_table,))]

    def get_max_date_for_ticker(self, ticker: str) -> datetime.date:
        """
        Возвращает максимальную дату для указанного тикера.
        """
        query = """
        SELECT MAX(date) 
        FROM securities_data 
        WHERE secid = %s
        """
        result = self.pg_client.execute(query, (ticker,))
        return result[0][0] if result and result[0][0] else None

    def insert_data(self, columns: List[str], rows: List[Dict]):
        """
        Вставляет данные в основную таблицу.
        """
        # Добавляем ticker в список колонок если его нет
        if 'secid' not in columns:
            columns.insert(0, 'secid')

        # Формируем SQL запрос
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT (secid, date) DO NOTHING").format(
            sql.Identifier(self.main_table),
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

    async def download_csv(self, bucket_name: str, file_key: str) -> str:
        """
        Загружает CSV файл из S3.
        """
        async with self.s3_client.get_client() as client:
            response = await client.get_object(Bucket=bucket_name, Key=file_key)
            async with response["Body"] as stream:
                return (await stream.read()).decode("utf-8")
