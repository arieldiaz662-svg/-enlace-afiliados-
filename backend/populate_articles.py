#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import models and services
from services.database import db_service


async def populate_articles():
    """Populate the database with blog articles"""
    
    # Connect to database
    await db_service.connect()
    
    try:
        # Clear existing articles
        await db_service.db.articles.delete_many({})
        
        print("✅ Cleared existing articles")
        
        # Insert Articles
        articles_data = [
            {
                "title": {
                    "es": "Los 5 mejores cepillos de dientes de bambú en 2025",
                    "en": "The 5 Best Bamboo Toothbrushes in 2025"
                },
                "slug": "mejores-cepillos-bambu-2025",
                "content": {
                    "es": """<p>¿Estás buscando una alternativa ecológica a los cepillos de plástico? Aquí te presentamos los mejores cepillos de bambú del 2025 según calidad, sostenibilidad y opiniones.</p>

<p>Los cepillos de dientes de bambú han revolucionado la higiene dental sostenible. Con más de 5 mil millones de cepillos de plástico desechados anualmente, cambiar a bambú es una decisión que impacta positivamente el medio ambiente.</p>

<h3>¿Por qué elegir cepillos de bambú?</h3>
<ul>
<li><strong>Biodegradables:</strong> El mango se descompone en 2-3 años</li>
<li><strong>Antimicrobianos:</strong> El bambú tiene propiedades naturales antibacterianas</li>
<li><strong>Sostenibles:</strong> El bambú crece hasta 35% más rápido que los árboles</li>
<li><strong>Cero residuos:</strong> Empaquetado sin plásticos</li>
</ul>

<p><strong>Consejo:</strong> Recuerda cambiar tu cepillo cada 3 meses y compostar el mango una vez termines su uso.</p>""",
                    "en": """<p>Looking for an eco-friendly alternative to plastic brushes? Here we present the best bamboo brushes of 2025 based on quality, sustainability and reviews.</p>

<p>Bamboo toothbrushes have revolutionized sustainable dental hygiene. With over 5 billion plastic brushes discarded annually, switching to bamboo is a decision that positively impacts the environment.</p>

<h3>Why choose bamboo brushes?</h3>
<ul>
<li><strong>Biodegradable:</strong> The handle decomposes in 2-3 years</li>
<li><strong>Antimicrobial:</strong> Bamboo has natural antibacterial properties</li>
<li><strong>Sustainable:</strong> Bamboo grows up to 35% faster than trees</li>
<li><strong>Zero waste:</strong> Packaging without plastics</li>
</ul>

<p><strong>Tip:</strong> Remember to change your brush every 3 months and compost the handle once you finish using it.</p>"""
                },
                "excerpt": {
                    "es": "Descubre los mejores cepillos de dientes de bambú del 2025. Guía completa con recomendaciones basadas en calidad, sostenibilidad y opiniones de usuarios.",
                    "en": "Discover the best bamboo toothbrushes of 2025. Complete guide with recommendations based on quality, sustainability and user reviews."
                },
                "category": "cepillos-bambu",
                "products": [
                    {
                        "title": "Cepillo de Bambú Humble Co.",
                        "description": "Cerdas suaves, certificado cruelty-free y empaquetado sin plástico.",
                        "amazon_link": "https://www.amazon.es/dp/B0829FNN5V?tag=bambugoods-21",
                        "position": 1
                    },
                    {
                        "title": "Cepillo Natural de EcoBamboo",
                        "description": "Mango ergonómico, ideal para adultos y niños, biodegradables al 95%.",
                        "amazon_link": "https://www.amazon.es/dp/B07C5TC92T?tag=bambugoods-21",
                        "position": 2
                    },
                    {
                        "title": "Set Familiar de Greenzla",
                        "description": "Pack de 6 cepillos, buena relación calidad-precio y empaque reciclado.",
                        "amazon_link": "https://www.amazon.es/dp/B07Q2D9C77?tag=bambugoods-21",
                        "position": 3
                    },
                    {
                        "title": "Cepillo de Bambú Isshah",
                        "description": "Diseño minimalista, cerdas suaves sin BPA, buena durabilidad.",
                        "amazon_link": "https://www.amazon.es/dp/B075V8X3CV?tag=bambugoods-21",
                        "position": 4
                    },
                    {
                        "title": "Cepillo ecológico Bambaw",
                        "description": "Empaque 100% compostable, opción vegana, viene con cerdas de carbón activado.",
                        "amazon_link": "https://www.amazon.es/dp/B076FQZ9H1?tag=bambugoods-21",
                        "position": 5
                    }
                ],
                "featured_image": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=800&h=600&fit=crop",
                "tags": ["cepillos bambú", "higiene sostenible", "cero residuos", "productos ecológicos"],
                "author": "BambuGoods Team",
                "is_published": True,
                "published_date": datetime.utcnow(),
                "seo_title": {
                    "es": "Los 5 Mejores Cepillos de Bambú 2025 - Guía Completa",
                    "en": "The 5 Best Bamboo Toothbrushes 2025 - Complete Guide"
                },
                "seo_description": {
                    "es": "Descubre los mejores cepillos de dientes de bambú del 2025. Comparativa completa con enlaces directos a Amazon. ¡Haz el cambio sostenible hoy!",
                    "en": "Discover the best bamboo toothbrushes of 2025. Complete comparison with direct Amazon links. Make the sustainable change today!"
                }
            },
            {
                "title": {
                    "es": "Champús Sólidos: La Revolución Natural para tu Cabello",
                    "en": "Solid Shampoos: The Natural Revolution for Your Hair"
                },
                "slug": "champu-solido-guia-completa",
                "content": {
                    "es": """<p>Los champús sólidos han llegado para quedarse. Más que una tendencia, representan una revolución hacia la cosmética sostenible y libre de químicos agresivos.</p>

<h3>¿Qué hace especial a un champú sólido?</h3>
<p>A diferencia de los champús líquidos tradicionales, los champús sólidos están concentrados y libres de agua, lo que significa:</p>

<ul>
<li><strong>Duración prolongada:</strong> Un champú sólido equivale a 2-3 botellas de champú líquido</li>
<li><strong>Sin conservantes:</strong> Al no contener agua, no necesitan conservantes químicos</li>
<li><strong>Zero waste:</strong> Empaquetado en papel o sin empaque</li>
<li><strong>Viaje friendly:</strong> No cuenta como líquido en el equipaje de mano</li>
</ul>

<h3>Cómo usar champú sólido correctamente</h3>
<ol>
<li>Moja tu cabello completamente</li>
<li>Frota el champú entre tus manos húmedas o directamente en el cabello</li>
<li>Masajea el cuero cabelludo suavemente</li>
<li>Aclara abundantemente</li>
<li>Guarda en lugar seco entre usos</li>
</ol>""",
                    "en": """<p>Solid shampoos are here to stay. More than a trend, they represent a revolution towards sustainable cosmetics free of harsh chemicals.</p>

<h3>What makes a solid shampoo special?</h3>
<p>Unlike traditional liquid shampoos, solid shampoos are concentrated and water-free, which means:</p>

<ul>
<li><strong>Extended duration:</strong> One solid shampoo equals 2-3 bottles of liquid shampoo</li>
<li><strong>No preservatives:</strong> As they contain no water, they don't need chemical preservatives</li>
<li><strong>Zero waste:</strong> Packaged in paper or without packaging</li>
<li><strong>Travel friendly:</strong> Doesn't count as liquid in carry-on luggage</li>
</ul>

<h3>How to use solid shampoo correctly</h3>
<ol>
<li>Wet your hair completely</li>
<li>Rub the shampoo between your wet hands or directly on hair</li>
<li>Massage the scalp gently</li>
<li>Rinse thoroughly</li>
<li>Store in a dry place between uses</li>
</ol>"""
                },
                "excerpt": {
                    "es": "Todo lo que necesitas saber sobre champús sólidos: beneficios, cómo usarlos y los mejores productos del mercado.",
                    "en": "Everything you need to know about solid shampoos: benefits, how to use them and the best products on the market."
                },
                "category": "champu-solido",
                "products": [
                    {
                        "title": "Champú Sólido Lush Honey I Washed My Hair",
                        "description": "Con miel y aceites naturales, ideal para cabello seco y dañado.",
                        "amazon_link": "https://www.amazon.es/dp/B084GHN123?tag=bambugoods-21",
                        "position": 1
                    },
                    {
                        "title": "Champú Sólido Natural Garnier",
                        "description": "Fórmula vegana con aceite de coco, para cabello graso.",
                        "amazon_link": "https://www.amazon.es/dp/B089SDG456?tag=bambugoods-21",
                        "position": 2
                    }
                ],
                "featured_image": "https://images.unsplash.com/photo-1556228578-dd4b84e0b8e8?w=800&h=600&fit=crop",
                "tags": ["champú sólido", "cosmética natural", "zero waste", "cabello natural"],
                "author": "BambuGoods Team",
                "is_published": True,
                "published_date": datetime.utcnow(),
                "seo_title": {
                    "es": "Champús Sólidos 2025 - Guía Completa y Mejores Productos",
                    "en": "Solid Shampoos 2025 - Complete Guide and Best Products"
                },
                "seo_description": {
                    "es": "Descubre todo sobre champús sólidos: beneficios, uso correcto y los mejores productos naturales del 2025. ¡Cambia a cosmética sostenible!",
                    "en": "Discover everything about solid shampoos: benefits, correct use and the best natural products of 2025. Switch to sustainable cosmetics!"
                }
            }
        ]
        
        for article_data in articles_data:
            await db_service.insert_one("articles", article_data)
        
        print("✅ Inserted articles")
        
        # Create text indexes for search
        await db_service.create_text_index("articles", ["title.es", "title.en", "content.es", "content.en", "tags"])
        
        print("✅ Created article search indexes")
        
        print(f"\n🎉 Articles populated successfully!")
        print(f"   📝 Articles: {len(articles_data)}")
        
    except Exception as e:
        print(f"❌ Error populating articles: {str(e)}")
        raise
    finally:
        await db_service.disconnect()


if __name__ == "__main__":
    asyncio.run(populate_articles())