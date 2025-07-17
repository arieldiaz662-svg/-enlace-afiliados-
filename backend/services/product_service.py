from typing import List, Optional
from bson import ObjectId
from models.product import Product, ProductCreate, ProductUpdate, ProductResponse
from services.database import db_service
import logging

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self):
        self.collection_name = "products"

    async def create_product(self, product_data: ProductCreate) -> Product:
        try:
            product_dict = product_data.dict(by_alias=True, exclude_unset=True)
            result = await db_service.insert_one(self.collection_name, product_dict)
            
            created_product = await db_service.find_one(
                self.collection_name, 
                {"_id": result.inserted_id}
            )
            return Product(**created_product)
        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            raise

    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        try:
            if not ObjectId.is_valid(product_id):
                return None
                
            product_data = await db_service.find_one(
                self.collection_name,
                {"_id": ObjectId(product_id)}
            )
            
            if product_data:
                return Product(**product_data)
            return None
        except Exception as e:
            logger.error(f"Error getting product by ID: {str(e)}")
            raise

    async def get_products(
        self, 
        category: Optional[str] = None,
        language: str = "es",
        search: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[ProductResponse]:
        try:
            filter_dict = {"is_active": True}
            
            if category:
                filter_dict["category"] = category
                
            if search:
                filter_dict["$or"] = [
                    {f"name.{language}": {"$regex": search, "$options": "i"}},
                    {f"description.{language}": {"$regex": search, "$options": "i"}},
                    {f"features.{language}": {"$in": [{"$regex": search, "$options": "i"}]}}
                ]
            
            products_data = await db_service.find_many(
                self.collection_name,
                filter_dict,
                limit=limit,
                skip=skip
            )
            
            # Transform products to localized response
            products = []
            for product_data in products_data:
                product = Product(**product_data)
                localized_product = ProductResponse(
                    id=str(product.id),
                    name=product.name.dict()[language],
                    description=product.description.dict()[language],
                    category=product.category,
                    price=product.price,
                    originalPrice=product.original_price,
                    image=product.image,
                    amazonLink=product.amazon_link,
                    rating=product.rating,
                    reviews=product.reviews,
                    features=product.features.get(language, []),
                    isActive=product.is_active,
                    createdAt=product.created_at,
                    updatedAt=product.updated_at
                )
                products.append(localized_product)
            
            return products
        except Exception as e:
            logger.error(f"Error getting products: {str(e)}")
            raise

    async def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[Product]:
        try:
            if not ObjectId.is_valid(product_id):
                return None
                
            update_dict = product_data.dict(by_alias=True, exclude_unset=True)
            
            result = await db_service.update_one(
                self.collection_name,
                {"_id": ObjectId(product_id)},
                update_dict
            )
            
            if result.modified_count:
                return await self.get_product_by_id(product_id)
            return None
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            raise

    async def delete_product(self, product_id: str) -> bool:
        try:
            if not ObjectId.is_valid(product_id):
                return False
                
            result = await db_service.delete_one(
                self.collection_name,
                {"_id": ObjectId(product_id)}
            )
            
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            raise

    async def get_products_count(self, category: Optional[str] = None, search: Optional[str] = None) -> int:
        try:
            filter_dict = {"is_active": True}
            
            if category:
                filter_dict["category"] = category
                
            if search:
                filter_dict["$or"] = [
                    {"name.es": {"$regex": search, "$options": "i"}},
                    {"name.en": {"$regex": search, "$options": "i"}},
                    {"description.es": {"$regex": search, "$options": "i"}},
                    {"description.en": {"$regex": search, "$options": "i"}}
                ]
            
            return await db_service.count_documents(self.collection_name, filter_dict)
        except Exception as e:
            logger.error(f"Error counting products: {str(e)}")
            raise


# Global product service instance
product_service = ProductService()