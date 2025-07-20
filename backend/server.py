from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Optional
from contextlib import asynccontextmanager

# Import models and services
from models.product import ProductCreate, ProductUpdate, ProductResponse
from models.category import CategoryCreate, CategoryResponse
from models.favorite import FavoriteCreate, FavoriteResponse
from models.article import ArticleCreate, ArticleResponse, ArticleSummary
from services.database import db_service
from services.product_service import product_service
from services.article_service import article_service


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_service.connect()
    logging.info("Database connected successfully")
    yield
    # Shutdown
    await db_service.disconnect()
    logging.info("Database disconnected")


# Create the main app without a prefix
app = FastAPI(lifespan=lifespan)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Product endpoints
@api_router.get("/products", response_model=List[ProductResponse])
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    language: str = Query("es", description="Language for localization"),
    search: Optional[str] = Query(None, description="Search term"),
    limit: int = Query(50, ge=1, le=100, description="Number of products to return"),
    skip: int = Query(0, ge=0, description="Number of products to skip")
):
    """Get all products with optional filtering"""
    try:
        products = await product_service.get_products(
            category=category,
            language=language,
            search=search,
            limit=limit,
            skip=skip
        )
        return products
    except Exception as e:
        logging.error(f"Error getting products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving products")


@api_router.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    """Get a specific product by ID"""
    try:
        product = await product_service.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving product")


@api_router.post("/products", response_model=ProductResponse)
async def create_product(product_data: ProductCreate):
    """Create a new product"""
    try:
        product = await product_service.create_product(product_data)
        return ProductResponse(
            id=str(product.id),
            name=product.name.es,  # Default to Spanish
            description=product.description.es,
            category=product.category,
            price=product.price,
            originalPrice=product.original_price,
            image=product.image,
            amazonLink=product.amazon_link,
            rating=product.rating,
            reviews=product.reviews,
            features=product.features.get("es", []),
            isActive=product.is_active,
            createdAt=product.created_at,
            updatedAt=product.updated_at
        )
    except Exception as e:
        logging.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating product")


@api_router.put("/products/{product_id}")
async def update_product(product_id: str, product_data: ProductUpdate):
    """Update an existing product"""
    try:
        product = await product_service.update_product(product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating product")


@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """Delete a product"""
    try:
        success = await product_service.delete_product(product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting product")


# Categories endpoints
@api_router.get("/categories")
async def get_categories(language: str = Query("es", description="Language for localization")):
    """Get all categories"""
    try:
        categories_data = await db_service.find_many("categories", {"is_active": True})
        categories = []
        for category_data in categories_data:
            categories.append({
                "id": category_data["category_id"],
                "name": category_data["name"][language],
                "icon": category_data["icon"]
            })
        return categories
    except Exception as e:
        logging.error(f"Error getting categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving categories")


# Articles endpoints
@api_router.get("/articles", response_model=List[ArticleSummary])
async def get_articles(
    category: Optional[str] = Query(None, description="Filter by category"),
    language: str = Query("es", description="Language for localization"),
    limit: int = Query(20, ge=1, le=100, description="Number of articles to return"),
    skip: int = Query(0, ge=0, description="Number of articles to skip")
):
    """Get all published articles"""
    try:
        articles = await article_service.get_articles(
            category=category,
            language=language,
            limit=limit,
            skip=skip
        )
        return articles
    except Exception as e:
        logging.error(f"Error getting articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving articles")


@api_router.get("/articles/{slug}", response_model=ArticleResponse)
async def get_article_by_slug(
    slug: str,
    language: str = Query("es", description="Language for localization")
):
    """Get a specific article by slug"""
    try:
        article = await article_service.get_article_by_slug(slug, language)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting article: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving article")


@api_router.get("/articles/{article_id}/related", response_model=List[ArticleSummary])
async def get_related_articles(
    article_id: str,
    language: str = Query("es", description="Language for localization"),
    limit: int = Query(3, ge=1, le=10, description="Number of related articles to return")
):
    """Get related articles by category"""
    try:
        # First get the article to find its category
        article_data = await db_service.find_one("articles", {"_id": ObjectId(article_id)})
        if not article_data:
            raise HTTPException(status_code=404, detail="Article not found")
        
        related_articles = await article_service.get_related_articles(
            category=article_data["category"],
            current_article_id=article_id,
            language=language,
            limit=limit
        )
        return related_articles
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting related articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving related articles")


# Favorites endpoints
@api_router.get("/favorites/{user_id}")
async def get_user_favorites(user_id: str):
    """Get user's favorite products"""
    try:
        favorites_data = await db_service.find_many("favorites", {"user_id": user_id})
        product_ids = [fav["product_id"] for fav in favorites_data]
        return {"favorites": [str(pid) for pid in product_ids]}
    except Exception as e:
        logging.error(f"Error getting favorites: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving favorites")


@api_router.post("/favorites")
async def add_favorite(favorite_data: FavoriteCreate):
    """Add product to favorites"""
    try:
        from bson import ObjectId
        
        # Check if already favorited
        existing = await db_service.find_one("favorites", {
            "user_id": favorite_data.user_id,
            "product_id": ObjectId(favorite_data.product_id)
        })
        
        if existing:
            return {"message": "Product already in favorites"}
        
        favorite_dict = {
            "user_id": favorite_data.user_id,
            "product_id": ObjectId(favorite_data.product_id),
            "created_at": datetime.utcnow()
        }
        
        await db_service.insert_one("favorites", favorite_dict)
        return {"message": "Product added to favorites"}
    except Exception as e:
        logging.error(f"Error adding favorite: {str(e)}")
        raise HTTPException(status_code=500, detail="Error adding favorite")


@api_router.delete("/favorites/{user_id}/{product_id}")
async def remove_favorite(user_id: str, product_id: str):
    """Remove product from favorites"""
    try:
        from bson import ObjectId
        
        result = await db_service.delete_one("favorites", {
            "user_id": user_id,
            "product_id": ObjectId(product_id)
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Favorite not found")
        
        return {"message": "Product removed from favorites"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error removing favorite: {str(e)}")
        raise HTTPException(status_code=500, detail="Error removing favorite")


# Search endpoints
@api_router.get("/search")
async def search_products(
    q: str = Query(..., description="Search query"),
    language: str = Query("es", description="Language for search"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")
):
    """Search products"""
    try:
        products = await product_service.get_products(
            category=category,
            language=language,
            search=q,
            limit=limit
        )
        return products
    except Exception as e:
        logging.error(f"Error searching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching products")


@api_router.get("/search/articles")
async def search_articles(
    q: str = Query(..., description="Search query"),
    language: str = Query("es", description="Language for search"),
    limit: int = Query(10, ge=1, le=50, description="Number of results to return")
):
    """Search articles"""
    try:
        articles = await article_service.search_articles(
            query=q,
            language=language,
            limit=limit
        )
        return articles
    except Exception as e:
        logging.error(f"Error searching articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching articles")


# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "BambuGoods API is running", "version": "1.0.0"}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import datetime for favorites
from datetime import datetime
from bson import ObjectId
