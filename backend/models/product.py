from pydantic import BaseModel, Field
from typing import List, Optional, Dict
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


class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: TranslatedField
    description: TranslatedField
    category: str
    price: float
    original_price: float = Field(alias="originalPrice")
    image: str
    amazon_link: str = Field(alias="amazonLink")
    rating: float
    reviews: int
    features: Dict[str, List[str]]
    is_active: bool = Field(default=True, alias="isActive")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProductCreate(BaseModel):
    name: TranslatedField
    description: TranslatedField
    category: str
    price: float
    original_price: float = Field(alias="originalPrice")
    image: str
    amazon_link: str = Field(alias="amazonLink")
    rating: float
    reviews: int
    features: Dict[str, List[str]]
    is_active: bool = Field(default=True, alias="isActive")

    class Config:
        allow_population_by_field_name = True


class ProductUpdate(BaseModel):
    name: Optional[TranslatedField] = None
    description: Optional[TranslatedField] = None
    category: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = Field(None, alias="originalPrice")
    image: Optional[str] = None
    amazon_link: Optional[str] = Field(None, alias="amazonLink")
    rating: Optional[float] = None
    reviews: Optional[int] = None
    features: Optional[Dict[str, List[str]]] = None
    is_active: Optional[bool] = Field(None, alias="isActive")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")

    class Config:
        allow_population_by_field_name = True


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: float
    originalPrice: float
    image: str
    amazonLink: str
    rating: float
    reviews: int
    features: List[str]
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        allow_population_by_field_name = True