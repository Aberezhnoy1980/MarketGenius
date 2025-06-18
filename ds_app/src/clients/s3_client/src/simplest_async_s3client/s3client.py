import os
from contextlib import asynccontextmanager

from aiobotocore.session import get_session


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
            bucket_name: str
    ):
        object_name = os.path.split(file_path)[-1]
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=bucket_name,
                    Key=object_name,
                    Body=file
                )

    #
    async def create_bucket(
            self,
            bucket_name: str,
    ):
        async with self.get_client() as client:
            await client.create_bucket(
                Bucket=bucket_name
            )

    async def get_object_list(
            self,
            bucket_name: str,
    ):
        async with self.get_client() as client:
            list_objs = await client.list_objects(Bucket=bucket_name)
            return list_objs["Contents"]

    async def get_object(
            self,
            bucket_name: str,
            key: str,
            file_path: str,
    ):
        async with self.get_client() as client:
            with open(os.path.join(file_path, key), "wb") as file:
                response = await client.get_object(Bucket=bucket_name, Key=key)
                async with response['Body'] as stream:
                    # await stream.read()
                    file.write(await stream.read())

            return f'"HTTPStatusCode": {response["ResponseMetadata"]["HTTPStatusCode"]}'

    async def delete_objects(
            self,
            bucket_name: str,
            objects: list[dict[str, str]]
    ):
        async with self.get_client() as client:
            response = await client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})
            return response
