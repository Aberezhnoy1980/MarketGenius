import asyncio
import os

from src.clients.s3_client.src.simplest_async_s3client.s3client import S3Client

your_access_key = 'access_key'
your_secret_key = 'secret_key'
your_endpoint_url = 'endpoint_url'

s3_client = S3Client(
    access_key="aVJiW_AWG0kBjK5ym6GfWKUvKXanLrJY",
    secret_key="u6mo70SME446xOCpSIINqlidwOyBUNMq",
    endpoint_url="https://api.immers.cloud:8080",
)

file_path = '/Users/alex/Documents/Study/Career/MIPT/FQW/features_final/ASTR_final.csv'
bucket_name = 'mldata'


async def upload_file(file_path, bucket_name):
    await s3_client.upload_file(file_path, bucket_name)


# asyncio.run(upload_file(file_path, bucket_name))


async def get_file(bucket, file_name):
    response = await s3_client.get_object(bucket, file_name, ".")
    print(response)


# asyncio.run(get_file('mldata', 'ASTR_final.csv'))

async def delete_all(bucket):
    objects = await s3_client.get_object_list(bucket)
    objects_to_delete = []

    for obj in objects:
        objects_to_delete.append({'Key': obj['Key']})

    resp = await s3_client.delete_objects(bucket, objects_to_delete)
    print(resp['ResponseMetadata']['HTTPStatusCode'])


# asyncio.run(delete_all(bucket_name))

async def upload_files(dir_path, bucket):
    files_list = os.listdir(dir_path)
    file_paths = [os.path.join(dir_path, file) for file in files_list]

    for file_path in file_paths:
        await s3_client.upload_file(file_path, bucket)


dir_path = '/Users/alex/Documents/Study/Career/MIPT/FQW/features_last'


# asyncio.run(upload_files(dir_path, bucket_name))

async def get_file_list(bucket):
    obj_list = await s3_client.get_object_list(bucket)

    for item in obj_list:
        print(item["Key"], item["Size"])


asyncio.run(get_file_list(bucket_name))
