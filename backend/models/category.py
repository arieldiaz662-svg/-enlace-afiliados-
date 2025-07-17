from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


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
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class TranslatedField(BaseModel):
    es: str
    en: str


class Category(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    category_id: str = Field(alias="categoryId")
    name: TranslatedField
    icon: str
    is_active: bool = Field(default=True, alias="isActive")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CategoryCreate(BaseModel):
    category_id: str = Field(alias="categoryId")
    name: TranslatedField
    icon: str
    is_active: bool = Field(default=True, alias="isActive")

    class Config:
        allow_population_by_field_name = True


class CategoryResponse(BaseModel):
    id: str
    name: str
    icon: str
    isActive: bool
    createdAt: datetime

    class Config:
        allow_population_by_field_name = True