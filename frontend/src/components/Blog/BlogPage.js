import React, { useState } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { useArticles } from '../../hooks/useArticles';
import { useCategories } from '../../hooks/useCategories';
import { Calendar, User, Tag, ExternalLink, Filter, Loader2, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

const BlogPage = () => {
  const { language, t } = useLanguage();
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  const { articles, loading: articlesLoading, error: articlesError } = useArticles(selectedCategory, language);
  const { categories, loading: categoriesLoading } = useCategories(language);

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

  const ArticleCard = ({ article }) => (
    <article className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-300 overflow-hidden group">
      <div className="relative">
        <img 
          src={article.featuredImage} 
          alt={article.title}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/400x200?text=BambuGoods+Blog';
          }}
        />
        <div className="absolute top-4 left-4">
          <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium">
            Blog
          </span>
        </div>
      </div>
      
      <div className="p-6">
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <Calendar className="h-4 w-4 mr-2" />
          <span>{formatDate(article.publishedDate)}</span>
          <User className="h-4 w-4 ml-4 mr-2" />
          <span>{article.author}</span>
        </div>
        
        <Link 
          to={`/blog/${article.slug}`}
          className="block group-hover:text-green-600 transition-colors duration-200"
        >
          <h2 className="text-xl font-bold text-gray-800 mb-3 line-clamp-2">
            {article.title}
          </h2>
        </Link>
        
        <p className="text-gray-600 mb-4 line-clamp-3">
          {article.excerpt}
        </p>
        
        <div className="flex flex-wrap gap-2 mb-4">
          {article.tags.slice(0, 3).map((tag, index) => (
            <span 
              key={index}
              className="inline-flex items-center bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs"
            >
              <Tag className="h-3 w-3 mr-1" />
              {tag}
            </span>
          ))}
        </div>
        
        <Link 
          to={`/blog/${article.slug}`}
          className="inline-flex items-center text-green-600 hover:text-green-700 font-medium transition-colors duration-200"
        >
          {language === 'es' ? 'Leer más' : 'Read more'}
          <ExternalLink className="h-4 w-4 ml-1" />
        </Link>
      </div>
    </article>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-50 via-emerald-50 to-green-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-green-800 mb-6">
            {language === 'es' ? 'Blog EcoSostenible' : 'EcoSustainable Blog'}
          </h1>
          <p className="text-xl text-green-700 max-w-3xl mx-auto">
            {language === 'es' 
              ? 'Guías, consejos y recomendaciones para un estilo de vida más sostenible y libre de químicos'
              : 'Guides, tips and recommendations for a more sustainable and chemical-free lifestyle'
            }
          </p>
        </div>
      </section>

      {/* Filter Section */}
      <section className="py-8 bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-5 w-5 text-gray-600" />
              <span className="text-gray-700 font-medium">{t('filterBy')}:</span>
            </div>
            
            {categoriesLoading ? (
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin text-green-600" />
                <span className="text-gray-500">Cargando categorías...</span>
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedCategory('all')}
                  className={`px-4 py-2 rounded-full font-medium transition-colors duration-200 ${
                    selectedCategory === 'all'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {t('allCategories')}
                </button>
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.id)}
                    className={`px-4 py-2 rounded-full font-medium transition-colors duration-200 ${
                      selectedCategory === category.id
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {category.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Articles Section */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-800">
              {language === 'es' ? 'Artículos Recientes' : 'Recent Articles'}
            </h2>
            <div className="flex items-center text-gray-500">
              <Clock className="h-4 w-4 mr-2" />
              <span className="text-sm">
                {language === 'es' ? 'Actualizado regularmente' : 'Updated regularly'}
              </span>
            </div>
          </div>
          
          {articlesError && <ErrorMessage message={articlesError} />}
          
          {articlesLoading ? (
            <LoadingSpinner />
          ) : articles.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">
                {language === 'es' ? 'No se encontraron artículos' : 'No articles found'}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {articles.map((article) => (
                <ArticleCard key={article.id} article={article} />
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default BlogPage;