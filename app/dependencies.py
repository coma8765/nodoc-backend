import io
import logging
import os
from typing import Any, AsyncGenerator

import aioboto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs import DB_URI

engine: Any = None
session: Any = None


class S3:
    s3: Any
    is_connected = False

    def __init__(self):
        self.session = aioboto3.Session()
        self.__s3 = self.session.client(
            "s3",
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            endpoint_url=os.getenv("S3_URI"),
            use_ssl=False,
        )

    async def connect(self):
        if self.is_connected:
            return
        self.is_connected = True
        self.s3 = await self.__s3.__aenter__()

    async def get_doc(self, user_id: int, doc_id: int) -> AsyncGenerator[bytes, None]:
        assert isinstance(user_id, int)
        assert isinstance(doc_id, int)

        try:
            obj = await self.s3.get_object(Bucket="docs", Key=f"{user_id}/{doc_id}")
        except Exception:
            raise Exception("Doc not found")
        async with obj["Body"] as f:
            yield await f.read(1024 * 60)

    async def upload_doc(self, user_id: int, doc_id: int, stream: io.BytesIO) -> bool:
        assert isinstance(user_id, int)
        assert isinstance(doc_id, int)

        try:
            await self.s3.upload_fileobj(stream, "docs", f"{user_id}/{doc_id}")
            return True
        except Exception as e:
            logging.getLogger(__name__).exception(e)
            return False

    async def shutdown(self):
        pass


s3 = S3()


async def startup():
    await s3.connect()

    global engine, session
    engine = engine or create_engine(DB_URI)
    session = session or sessionmaker(bind=engine, expire_on_commit=False)


async def shutdown():
    await s3.shutdown()


__all__ = ["startup", "shutdown", "s3", "engine", "session"]
