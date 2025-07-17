import React, { useState, useEffect } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { useProducts } from '../../hooks/useProducts';
import { useCategories } from '../../hooks/useCategories';
import { useFavorites } from '../../hooks/useFavorites';
import { Star, ExternalLink, Heart, Filter, Leaf, Recycle, Award, Shield, Loader2 } from 'lucide-react';

const HomePage = () => {
  const { language, t } = useLanguage();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  const { products, loading: productsLoading, error: productsError } = useProducts(selectedCategory, language, searchTerm);
  const { categories, loading: categoriesLoading } = useCategories(language);
  const { favorites, toggleFavorite, isFavorite, loading: favoritesLoading } = useFavorites();

  const renderStars = (rating) => {
    return [...Array(5)].map((_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${i < Math.floor(rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
      />
    ));
  };

  const HeroSection = () => (
    <section className="bg-gradient-to-br from-green-50 via-emerald-50 to-green-100 py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="bg-green-600 p-4 rounded-full">
              <Leaf className="h-12 w-12 text-white" />
            </div>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-green-800 mb-6">
            {t('title')}
          </h1>
          <p className="text-xl md:text-2xl text-green-700 mb-8 max-w-3xl mx-auto">
            {t('subtitle')}
          </p>
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <div className="flex items-center space-x-2 bg-white px-4 py-2 rounded-full shadow-sm">
              <Recycle className="h-5 w-5 text-green-600" />
              <span className="text-green-700 font-medium">{t('ecoFriendly')}</span>
            </div>
            <div className="flex items-center space-x-2 bg-white px-4 py-2 rounded-full shadow-sm">
              <Shield className="h-5 w-5 text-green-600" />
              <span className="text-green-700 font-medium">{t('naturalIngredients')}</span>
            </div>
            <div className="flex items-center space-x-2 bg-white px-4 py-2 rounded-full shadow-sm">
              <Award className="h-5 w-5 text-green-600" />
              <span className="text-green-700 font-medium">{t('plasticFree')}</span>
            </div>
          </div>
          <button 
            onClick={() => setSelectedCategory('all')}
            className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-full text-lg font-semibold transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            {t('allProducts')}
          </button>
        </div>
      </div>
    </section>
  );

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

  const ProductCard = ({ product }) => (
    <div className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-300 overflow-hidden group">
      <div className="relative">
        <img 
          src={product.image} 
          alt={product.name}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x300?text=BambuGoods';
          }}
        />
        <button
          onClick={() => toggleFavorite(product.id)}
          disabled={favoritesLoading}
          className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-shadow duration-200 disabled:opacity-50"
        >
          <Heart className={`h-5 w-5 ${isFavorite(product.id) ? 'text-red-500 fill-current' : 'text-gray-400'}`} />
        </button>
        <div className="absolute top-3 left-3 bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium">
          {t('ecoFriendly')}
        </div>
      </div>
      
      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 group-hover:text-green-600 transition-colors duration-200">
          {product.name}
        </h3>
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {product.description}
        </p>
        
        <div className="flex items-center mb-4">
          <div className="flex items-center space-x-1 mr-3">
            {renderStars(product.rating)}
          </div>
          <span className="text-sm text-gray-500">
            {product.rating} ({product.reviews} {t('rating')})
          </span>
        </div>
        
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-green-600">€{product.price}</span>
            <span className="text-sm text-gray-500 line-through">€{product.originalPrice}</span>
          </div>
        </div>
        
        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">{t('features')}:</p>
          <div className="flex flex-wrap gap-1">
            {product.features.slice(0, 2).map((feature, index) => (
              <span key={index} className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">
                {feature}
              </span>
            ))}
          </div>
        </div>
        
        <button 
          onClick={() => window.open(product.amazonLink, '_blank')}
          className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          <span>{t('buyOnAmazon')}</span>
          <ExternalLink className="h-4 w-4" />
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <HeroSection />
      
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

      {/* Products Section */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            {selectedCategory === 'all' ? t('allProducts') : t('featuredProducts')}
          </h2>
          
          {productsError && <ErrorMessage message={productsError} />}
          
          {productsLoading ? (
            <LoadingSpinner />
          ) : products.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">{t('noResults')}</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default HomePage;