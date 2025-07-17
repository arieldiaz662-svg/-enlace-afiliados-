from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os


class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'bambugoods')
        
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def get_collection(self, collection_name: str):
        return self.db[collection_name]

    async def insert_one(self, collection_name: str, document: dict):
        collection = await self.get_collection(collection_name)
        result = await collection.insert_one(document)
        return result

    async def find_one(self, collection_name: str, filter_dict: dict):
        collection = await self.get_collection(collection_name)
        return await collection.find_one(filter_dict)

    async def find_many(self, collection_name: str, filter_dict: dict = None, limit: int = None, skip: int = None):
        collection = await self.get_collection(collection_name)
        cursor = collection.find(filter_dict or {})
        
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
            
        return await cursor.to_list(length=limit)

    async def update_one(self, collection_name: str, filter_dict: dict, update_dict: dict):
        collection = await self.get_collection(collection_name)
        result = await collection.update_one(filter_dict, {"$set": update_dict})
        return result

    async def delete_one(self, collection_name: str, filter_dict: dict):
        collection = await self.get_collection(collection_name)
        result = await collection.delete_one(filter_dict)
        return result

    async def count_documents(self, collection_name: str, filter_dict: dict = None):
        collection = await self.get_collection(collection_name)
        return await collection.count_documents(filter_dict or {})

    async def create_text_index(self, collection_name: str, fields: list):
        collection = await self.get_collection(collection_name)
        index_spec = [(field, "text") for field in fields]
        await collection.create_index(index_spec)


# Global database instance
db_service = DatabaseService()