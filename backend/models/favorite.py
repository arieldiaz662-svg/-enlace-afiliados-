from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Any


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _source_type: Any, _handler) -> dict:
        return {'type': 'string'}


class Favorite(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(alias="userId")
    product_id: PyObjectId = Field(alias="productId")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


class FavoriteCreate(BaseModel):
    user_id: str = Field(alias="userId")
    product_id: str = Field(alias="productId")

    model_config = {
        "populate_by_name": True
    }


class FavoriteResponse(BaseModel):
    id: str
    userId: str
    productId: str
    createdAt: datetime

    model_config = {
        "populate_by_name": True
    }