from typing import List, Optional
from bson import ObjectId
from models.article import Article, ArticleCreate, ArticleResponse, ArticleSummary
from services.database import db_service
import logging

logger = logging.getLogger(__name__)


class ArticleService:
    def __init__(self):
        self.collection_name = "articles"

    async def create_article(self, article_data: ArticleCreate) -> Article:
        try:
            article_dict = article_data.dict(by_alias=True, exclude_unset=True)
            result = await db_service.insert_one(self.collection_name, article_dict)
            
            created_article = await db_service.find_one(
                self.collection_name, 
                {"_id": result.inserted_id}
            )
            return Article(**created_article)
        except Exception as e:
            logger.error(f"Error creating article: {str(e)}")
            raise

    async def get_article_by_slug(self, slug: str, language: str = "es") -> Optional[ArticleResponse]:
        try:
            article_data = await db_service.find_one(
                self.collection_name,
                {"slug": slug, "is_published": True}
            )
            
            if article_data:
                article = Article(**article_data)
                return ArticleResponse(
                    id=str(article.id),
                    title=article.title.dict()[language],
                    slug=article.slug,
                    content=article.content.dict()[language],
                    excerpt=article.excerpt.dict()[language],
                    category=article.category,
                    products=article.products,
                    featuredImage=article.featured_image,
                    tags=article.tags,
                    author=article.author,
                    isPublished=article.is_published,
                    publishedDate=article.published_date,
                    createdAt=article.created_at,
                    updatedAt=article.updated_at,
                    seoTitle=article.seo_title.dict()[language],
                    seoDescription=article.seo_description.dict()[language]
                )
            return None
        except Exception as e:
            logger.error(f"Error getting article by slug: {str(e)}")
            raise

    async def get_articles(
        self, 
        category: Optional[str] = None,
        language: str = "es",
        limit: int = 20,
        skip: int = 0
    ) -> List[ArticleSummary]:
        try:
            filter_dict = {"is_published": True}
            
            if category:
                filter_dict["category"] = category
            
            articles_data = await db_service.find_many(
                self.collection_name,
                filter_dict,
                limit=limit,
                skip=skip
            )
            
            # Sort by published_date descending
            articles_data.sort(key=lambda x: x.get("published_date", x.get("created_at")), reverse=True)
            
            articles = []
            for article_data in articles_data:
                article = Article(**article_data)
                summary = ArticleSummary(
                    id=str(article.id),
                    title=article.title.dict()[language],
                    slug=article.slug,
                    excerpt=article.excerpt.dict()[language],
                    category=article.category,
                    featuredImage=article.featured_image,
                    tags=article.tags,
                    author=article.author,
                    publishedDate=article.published_date
                )
                articles.append(summary)
            
            return articles
        except Exception as e:
            logger.error(f"Error getting articles: {str(e)}")
            raise

    async def get_related_articles(
        self, 
        category: str, 
        current_article_id: str,
        language: str = "es",
        limit: int = 3
    ) -> List[ArticleSummary]:
        try:
            filter_dict = {
                "is_published": True,
                "category": category,
                "_id": {"$ne": ObjectId(current_article_id)}
            }
            
            articles_data = await db_service.find_many(
                self.collection_name,
                filter_dict,
                limit=limit
            )
            
            articles = []
            for article_data in articles_data:
                article = Article(**article_data)
                summary = ArticleSummary(
                    id=str(article.id),
                    title=article.title.dict()[language],
                    slug=article.slug,
                    excerpt=article.excerpt.dict()[language],
                    category=article.category,
                    featuredImage=article.featured_image,
                    tags=article.tags,
                    author=article.author,
                    publishedDate=article.published_date
                )
                articles.append(summary)
            
            return articles
        except Exception as e:
            logger.error(f"Error getting related articles: {str(e)}")
            raise

    async def search_articles(
        self,
        query: str,
        language: str = "es",
        limit: int = 10
    ) -> List[ArticleSummary]:
        try:
            filter_dict = {
                "is_published": True,
                "$or": [
                    {f"title.{language}": {"$regex": query, "$options": "i"}},
                    {f"content.{language}": {"$regex": query, "$options": "i"}},
                    {f"excerpt.{language}": {"$regex": query, "$options": "i"}},
                    {"tags": {"$in": [{"$regex": query, "$options": "i"}]}}
                ]
            }
            
            articles_data = await db_service.find_many(
                self.collection_name,
                filter_dict,
                limit=limit
            )
            
            articles = []
            for article_data in articles_data:
                article = Article(**article_data)
                summary = ArticleSummary(
                    id=str(article.id),
                    title=article.title.dict()[language],
                    slug=article.slug,
                    excerpt=article.excerpt.dict()[language],
                    category=article.category,
                    featuredImage=article.featured_image,
                    tags=article.tags,
                    author=article.author,
                    publishedDate=article.published_date
                )
                articles.append(summary)
            
            return articles
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            raise


# Global article service instance
article_service = ArticleService()