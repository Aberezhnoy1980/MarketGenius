import csv
from io import StringIO
from datetime import datetime
from src.clients.s3_client.src.simplest_async_s3client.s3client import S3Client
from src.clients.db_client.src.simplest_pg_client.pg_client import PostgresClient

from psycopg2 import sql


class S3ToPostgresETL:
    def __init__(self, s3_client: S3Client, pg_client: PostgresClient):
        self.s3_client = s3_client
        self.pg_client = pg_client

    async def process_bucket(self, bucket_name: str):
        objects = await self.s3_client.get_object_list(bucket_name)
        csv_files = [obj for obj in objects if obj["Key"].endswith(".csv")]

        for obj in csv_files:
            table_name = obj["Key"].replace(".csv", "")
            await self.process_file(bucket_name, obj["Key"], table_name)

    async def process_file(self, bucket_name: str, file_key: str, table_name: str):
        csv_content = await self.download_csv(bucket_name, file_key)
        reader = csv.DictReader(StringIO(csv_content))

        if not reader.fieldnames:
            print(f"Файл {file_key} пуст или некорректен.")
            return

        if not self.pg_client.table_exists(table_name):
            self.create_table(table_name, reader.fieldnames)
            max_date = None
        else:
            max_date = self.pg_client.get_max_date(table_name)

        rows_to_insert = []
        for row in reader:
            date_column = "date"  # или другая колонка с датой
            if date_column not in reader.fieldnames:
                raise ValueError(f"В файле {file_key} нет колонки {date_column}")
            row_date = datetime.strptime(row["date"], "%Y-%m-%d").date()  # Предполагаем колонку 'date'
            if max_date is None or row_date > max_date:
                rows_to_insert.append(row)

        if rows_to_insert:
            self.insert_data(table_name, reader.fieldnames, rows_to_insert)
            print(f"Добавлено {len(rows_to_insert)} записей в таблицу {table_name}.")
        else:
            print(f"Нет новых данных для таблицы {table_name}.")

    async def download_csv(self, bucket_name: str, file_key: str) -> str:
        async with self.s3_client.get_client() as client:
            response = await client.get_object(Bucket=bucket_name, Key=file_key)
            async with response["Body"] as stream:
                return (await stream.read()).decode("utf-8")

    def create_table(self, table_name: str, columns: list[str]):
        columns_sql = sql.SQL(", ").join(
            [sql.SQL("{} TEXT").format(sql.Identifier(col)) for col in columns]
        )
        query = sql.SQL("CREATE TABLE {} ({});").format(
            sql.Identifier(table_name),
            columns_sql
        )
        self.pg_client.execute(query)

    def insert_data(self, table_name: str, columns: list[str], rows: list[dict]):
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join([sql.Placeholder()] * len(columns))
        )
        with self.pg_client.get_cursor() as cursor:
            for row in rows:
                cursor.execute(query, [row[col] for col in columns])


import asyncio
import os
from dotenv import load_dotenv


async def main():
    # Переменные
    load_dotenv()

    # Инициализация клиентов
    s3_client = S3Client(
        access_key=os.getenv('access_key'),
        secret_key=os.getenv('secret_key'),
        endpoint_url=os.getenv('endpoint_url')
    )
    pg_client = PostgresClient(
        host=os.getenv('FEATURES_DB_HOST'),
        port=int(os.getenv('FEATURES_DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('FEATURE_DB_NAME')
    )

    # Запуск ETL
    etl = S3ToPostgresETL(s3_client, pg_client)
    await etl.process_bucket("mldata")


if __name__ == "__main__":
    asyncio.run(main())
