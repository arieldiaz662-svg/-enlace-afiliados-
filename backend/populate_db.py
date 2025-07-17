#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import models and services
from models.product import ProductCreate, TranslatedField
from models.category import CategoryCreate
from services.database import db_service


async def populate_database():
    """Populate the database with mock data"""
    
    # Connect to database
    await db_service.connect()
    
    try:
        # Clear existing data
        await db_service.db.products.delete_many({})
        await db_service.db.categories.delete_many({})
        await db_service.db.favorites.delete_many({})
        
        print("✅ Cleared existing data")
        
        # Insert Categories
        categories_data = [
            {
                "category_id": "cepillos-bambu",
                "name": {"es": "Cepillos de Bambú", "en": "Bamboo Brushes"},
                "icon": "Brush",
                "is_active": True
            },
            {
                "category_id": "champu-solido",
                "name": {"es": "Champús Sólidos", "en": "Solid Shampoos"},
                "icon": "Droplets",
                "is_active": True
            },
            {
                "category_id": "cuidado-facial",
                "name": {"es": "Cuidado Facial", "en": "Facial Care"},
                "icon": "Heart",
                "is_active": True
            },
            {
                "category_id": "kits-sostenibles",
                "name": {"es": "Kits Sostenibles", "en": "Sustainable Kits"},
                "icon": "Package",
                "is_active": True
            },
            {
                "category_id": "cuidado-personal",
                "name": {"es": "Cuidado Personal", "en": "Personal Care"},
                "icon": "User",
                "is_active": True
            },
            {
                "category_id": "cuidado-corporal",
                "name": {"es": "Cuidado Corporal", "en": "Body Care"},
                "icon": "Sparkles",
                "is_active": True
            }
        ]
        
        for category_data in categories_data:
            await db_service.insert_one("categories", category_data)
        
        print("✅ Inserted categories")
        
        # Insert Products
        products_data = [
            {
                "name": {
                    "es": "Cepillo de Dientes de Bambú Adulto",
                    "en": "Adult Bamboo Toothbrush"
                },
                "description": {
                    "es": "Cepillo de dientes biodegradable con cerdas de nylon libre de BPA. Mango 100% bambú sostenible.",
                    "en": "Biodegradable toothbrush with BPA-free nylon bristles. 100% sustainable bamboo handle."
                },
                "category": "cepillos-bambu",
                "price": 8.99,
                "original_price": 12.99,
                "image": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=300&h=300&fit=crop",
                "amazon_link": "https://amazon.es/dp/ejemplo1",
                "rating": 4.5,
                "reviews": 234,
                "features": {
                    "es": ["100% bambú sostenible", "Cerdas libres de BPA", "Biodegradable", "Empaque compostable"],
                    "en": ["100% sustainable bamboo", "BPA-free bristles", "Biodegradable", "Compostable packaging"]
                },
                "is_active": True
            },
            {
                "name": {
                    "es": "Champú Sólido Natural - Cabello Graso",
                    "en": "Natural Solid Shampoo - Oily Hair"
                },
                "description": {
                    "es": "Champú sólido natural con aceite de árbol de té y arcilla verde. Sin sulfatos, parabenos ni plásticos.",
                    "en": "Natural solid shampoo with tea tree oil and green clay. No sulfates, parabens or plastics."
                },
                "category": "champu-solido",
                "price": 11.99,
                "original_price": 15.99,
                "image": "https://images.unsplash.com/photo-1556228578-dd4b84e0b8e8?w=300&h=300&fit=crop",
                "amazon_link": "https://amazon.es/dp/ejemplo2",
                "rating": 4.7,
                "reviews": 189,
                "features": {
                    "es": ["Sin sulfatos", "Aceite de árbol de té", "Arcilla verde", "Duración 80 lavados"],
                    "en": ["Sulfate-free", "Tea tree oil", "Green clay", "80 washes duration"]
                },
                "is_active": True
            },
            {
                "name": {
                    "es": "Aceite Facial de Jojoba Orgánico",
                    "en": "Organic Jojoba Facial Oil"
                },
                "description": {
                    "es": "Aceite facial 100% puro de jojoba orgánico. Hidrata sin obstruir poros, ideal para todo tipo de piel.",
                    "en": "100% pure organic jojoba facial oil. Hydrates without clogging pores, ideal for all skin types."
                },
                "category": "cuidado-facial",
                "price": 14.99,
                "original_price": 18.99,
                "image": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=300&h=300&fit=crop",
                "amazon_link": "https://amazon.es/dp/ejemplo3",
                "rating": 4.8,
                "reviews": 156,
                "features": {
                    "es": ["100% orgánico", "Prensado en frío", "No comedogénico", "Botella de vidrio"],
                    "en": ["100% organic", "Cold-pressed", "Non-comedogenic", "Glass bottle"]
                },
                "is_active": True
            },
            {
                "name": {
                    "es": "Kit Sostenible de Higiene Personal",
                    "en": "Sustainable Personal Hygiene Kit"
                },
                "description": {
                    "es": "Kit completo con cepillo de bambú, champú sólido, jabón natural y bolsa de algodón orgánico.",
                    "en": "Complete kit with bamboo brush, solid shampoo, natural soap and organic cotton bag."
                },
                "category": "kits-sostenibles",
                "price": 24.99,
                "original_price": 35.99,
                "image": "https://images.unsplash.com/photo-1556228852-bf91b5b2f44d?w=300&h=300&fit=crop",
                "amazon_link": "https://amazon.es/dp/ejemplo4",
                "rating": 4.6,
                "reviews": 89,
                "features": {
                    "es": ["Kit completo", "Bolsa de algodón", "Productos naturales", "Perfecto para viajes"],
                    "en": ["Complete kit", "Cotton bag", "Natural products", "Perfect for travel"]
                },
                "is_active": True
            },
            {
                "name": {
                    "es": "Desodorante Natural Sin Aluminio",
                    "en": "Natural Aluminum-Free Deodorant"
                },
                "description": {
                    "es": "Desodorante natural con aceite de coco y bicarbonato. Sin aluminio, parabenos ni químicos agresivos.",
                    "en": "Natural deodorant with coconut oil and baking soda. No aluminum, parabens or harsh chemicals."
                },
                "category": "cuidado-personal",
                "price": 9.99,
                "original_price": 13.99,
                "image": "https://images.unsplash.com/photo-1556228847-0a5d1a6b0b7d?w=300&h=300&fit=crop",
                "amazon_link": "https://amazon.es/dp/ejemplo5",
                "rating": 4.4,
                "reviews": 203,
                "features": {
                    "es": ["Sin aluminio", "Aceite de coco", "Bicarbonato natural", "Envase biodegradable"],
                    "en": ["Aluminum-free", "Coconut oil", "Natural baking soda", "Biodegradable packaging"]
                },
                "is_active": True
            },
            {
                "name": {
                    "es": "Jabón Exfoliante de Café",
                    "en": "Coffee Exfoliating Soap"
                },
                "description": {
                    "es": "Jabón exfoliante natural con granos de café reciclados. Elimina células muertas y suaviza la piel.",
                    "en": "Natural exfoliating soap with recycled coffee grounds. Removes dead skin cells and softens skin."
                },
                "category": "cuidado-corporal",
                "price": 7.99,
                "original_price": 10.99,
                "image": "https://images.unsplash.com/photo-1556228847-0a5d1a6b0b7d?w=300&h=300&fit=crop",
                "amazon_link": "https://amazon.es/dp/ejemplo6",
                "rating": 4.3,
                "reviews": 167,
                "features": {
                    "es": ["Granos de café reciclados", "Exfoliante natural", "Aceites esenciales", "Vegano"],
                    "en": ["Recycled coffee grounds", "Natural exfoliant", "Essential oils", "Vegan"]
                },
                "is_active": True
            }
        ]
        
        for product_data in products_data:
            await db_service.insert_one("products", product_data)
        
        print("✅ Inserted products")
        
        # Create text indexes for search
        await db_service.create_text_index("products", ["name.es", "name.en", "description.es", "description.en"])
        
        print("✅ Created search indexes")
        
        print(f"\n🎉 Database populated successfully!")
        print(f"   📦 Categories: {len(categories_data)}")
        print(f"   🛍️  Products: {len(products_data)}")
        
    except Exception as e:
        print(f"❌ Error populating database: {str(e)}")
        raise
    finally:
        await db_service.disconnect()


if __name__ == "__main__":
    asyncio.run(populate_database())