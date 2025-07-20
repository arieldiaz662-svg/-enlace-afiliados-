from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _source_type: Any, _handler=None) -> dict:
        return {'type': 'string'}


class TranslatedField(BaseModel):
    es: str
    en: str


class ProductRecommendation(BaseModel):
    title: str
    description: str
    amazon_link: str = Field(alias="amazonLink")
    position: int

    model_config = {
        "populate_by_name": True
    }


class Article(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: TranslatedField
    slug: str
    content: TranslatedField
    excerpt: TranslatedField
    category: str  # "cepillos-bambu", "champu-solido", etc.
    products: List[ProductRecommendation]
    featured_image: str = Field(alias="featuredImage")
    tags: List[str]
    author: str
    is_published: bool = Field(default=True, alias="isPublished")
    published_date: datetime = Field(default_factory=datetime.utcnow, alias="publishedDate")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")
    seo_title: TranslatedField = Field(alias="seoTitle")
    seo_description: TranslatedField = Field(alias="seoDescription")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


class ArticleCreate(BaseModel):
    title: TranslatedField
    slug: str
    content: TranslatedField
    excerpt: TranslatedField
    category: str
    products: List[ProductRecommendation]
    featured_image: str = Field(alias="featuredImage")
    tags: List[str]
    author: str
    is_published: bool = Field(default=True, alias="isPublished")
    seo_title: TranslatedField = Field(alias="seoTitle")
    seo_description: TranslatedField = Field(alias="seoDescription")

    model_config = {
        "populate_by_name": True
    }


class ArticleResponse(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    excerpt: str
    category: str
    products: List[ProductRecommendation]
    featuredImage: str
    tags: List[str]
    author: str
    isPublished: bool
    publishedDate: datetime
    createdAt: datetime
    updatedAt: datetime
    seoTitle: str
    seoDescription: str

    model_config = {
        "populate_by_name": True
    }


class ArticleSummary(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str
    category: str
    featuredImage: str
    tags: List[str]
    author: str
    publishedDate: datetime

    model_config = {
        "populate_by_name": True
    }