import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { useArticle } from '../../hooks/useArticles';
import { Calendar, User, Tag, ExternalLink, ArrowLeft, Loader2, ShoppingBag } from 'lucide-react';

const ArticlePage = () => {
  const { slug } = useParams();
  const { language, t } = useLanguage();
  const { article, loading, error } = useArticle(slug, language);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(language === 'es' ? 'es-ES' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const LoadingSpinner = () => (
    <div className="flex items-center justify-center py-12">
      <Loader2 className="h-8 w-8 animate-spin text-green-600" />
      <span className="ml-2 text-green-700">{t('loading')}</span>
    </div>
  );

  const ErrorMessage = ({ message }) => (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <p className="text-red-700">{message}</p>
    </div>
  );

  const ProductRecommendation = ({ product, index }) => (
    <div className="bg-white border border-green-200 rounded-lg p-4 mb-4 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <span className="bg-green-500 text-white text-sm font-bold px-2 py-1 rounded-full mr-3">
              #{index + 1}
            </span>
            <h3 className="text-lg font-semibold text-gray-800">
              {product.title}
            </h3>
          </div>
          <p className="text-gray-600 mb-3">
            {product.description}
          </p>
        </div>
      </div>
      <a
        href={product.amazonLink}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
      >
        <ShoppingBag className="h-4 w-4 mr-2" />
        {language === 'es' ? 'Ver en Amazon' : 'View on Amazon'}
        <ExternalLink className="h-4 w-4 ml-2" />
      </a>
    </div>
  );

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!article) return <ErrorMessage message={language === 'es' ? 'Artículo no encontrado' : 'Article not found'} />;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Back Button */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link 
            to="/blog"
            className="inline-flex items-center text-green-600 hover:text-green-700 font-medium transition-colors duration-200"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            {language === 'es' ? 'Volver al Blog' : 'Back to Blog'}
          </Link>
        </div>
      </div>

      {/* Article Header */}
      <section className="bg-white py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center text-sm text-gray-500 mb-4">
              <Calendar className="h-4 w-4 mr-2" />
              <span>{formatDate(article.publishedDate)}</span>
              <User className="h-4 w-4 ml-6 mr-2" />
              <span>{article.author}</span>
            </div>
            
            <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
              {article.title}
            </h1>
            
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              {article.excerpt}
            </p>
            
            <div className="flex flex-wrap justify-center gap-2 mt-6">
              {article.tags.map((tag, index) => (
                <span 
                  key={index}
                  className="inline-flex items-center bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                >
                  <Tag className="h-3 w-3 mr-1" />
                  {tag}
                </span>
              ))}
            </div>
          </div>

          <div className="relative">
            <img 
              src={article.featuredImage} 
              alt={article.title}
              className="w-full h-64 md:h-96 object-cover rounded-lg shadow-lg"
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/800x400?text=BambuGoods+Blog';
              }}
            />
          </div>
        </div>
      </section>

      {/* Article Content */}
      <section className="py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-sm p-8">
            {/* Article Body */}
            <div 
              className="prose prose-lg max-w-none mb-12"
              dangerouslySetInnerHTML={{ __html: article.content }}
            />

            {/* Product Recommendations */}
            {article.products && article.products.length > 0 && (
              <div className="border-t border-gray-200 pt-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                  <ShoppingBag className="h-6 w-6 mr-3 text-green-600" />
                  {language === 'es' ? 'Productos Recomendados' : 'Recommended Products'}
                </h2>
                
                <div className="grid gap-6">
                  {article.products.map((product, index) => (
                    <ProductRecommendation 
                      key={index} 
                      product={product} 
                      index={index} 
                    />
                  ))}
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mt-6">
                  <p className="text-sm text-green-700">
                    <strong>{language === 'es' ? 'Nota:' : 'Note:'}</strong>{' '}
                    {language === 'es' 
                      ? 'BambuGoods es participante del Programa de Afiliación de Amazon. Las compras realizadas a través de nuestros enlaces pueden generar comisiones sin coste adicional para ti.'
                      : 'BambuGoods is a participant in the Amazon Affiliate Program. Purchases made through our links may generate commissions at no additional cost to you.'
                    }
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};

export default ArticlePage;