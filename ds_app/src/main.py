import asyncio
import os
from dotenv import load_dotenv
from tqdm import tqdm

# from src.S3ToPostgresETL.S3ToPostgresETL import S3ToPostgresETL
from src.S3ToPostgresETL.S3ToPostgresETLv2 import S3ToPostgresETL
from src.clients.db_client.src.simplest_pg_client.pg_client import PostgresClient
from src.clients.s3_client.src.simplest_async_s3client.s3client import S3Client


async def main():
    # Загрузка переменных окружения
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

    # table_name = "securities_data"
    table_name = "securities_data_1506"

    # Проверка соединений
    if not pg_client.check_connection():
        raise ConnectionError("Не удалось подключиться к PostgreSQL")

    # Запуск ETL процесса
    etl = S3ToPostgresETL(s3_client, pg_client, table_name, need_spec_check=False)
    await etl.process_bucket("mldata")

    # Финализируем кластеризацию
    pg_client.execute("CLUSTER securities_data USING securities_data_pkey")
    pg_client.execute("ANALYZE securities_data")


if __name__ == "__main__":
    asyncio.run(main())
