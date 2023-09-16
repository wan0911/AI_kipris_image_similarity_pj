""" fastapi용 mongo - pj에서 사용 X """

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

MONGO_DB_NAME = "markData"
MONGO_URL = ""

class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(client=self.client, database=MONGO_DB_NAME)
        print("DB와 성공적으로 연결이 되었습니다.")

    def close(self):
        self.client.close()
        print("bye server")


mongodb = MongoDB()
