import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { categories } from '../../data/mock';
import { Search, Globe, Menu, X, Leaf } from 'lucide-react';

const Header = () => {
  const { language, toggleLanguage, t } = useLanguage();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const currentCategories = categories[language];

  const handleSearch = (e) => {
    e.preventDefault();
    // Mock search functionality - in real app would filter products
    console.log('Searching for:', searchTerm);
  };

  const isActive = (path) => location.pathname === path;
  const isActiveCategory = (categoryId) => location.pathname.includes(`#${categoryId}`);

  return (
    <header className="bg-gradient-to-r from-green-50 to-emerald-50 shadow-sm border-b border-green-100">
      {/* Top bar */}
      <div className="bg-green-600 text-white py-2 px-4 text-center text-sm">
        <span className="font-medium">🌿 {t('ecoFriendly')} • {t('naturalIngredients')} • {t('plasticFree')}</span>
      </div>

      {/* Main header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-green-600 p-2 rounded-full">
              <Leaf className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-green-700">{t('title')}</h1>
              <p className="text-sm text-green-600 hidden sm:block">{t('subtitle')}</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <Link
              to="/"
              className={`font-medium transition-colors duration-200 hover:underline underline-offset-4 ${
                isActive('/') ? 'text-green-900 underline' : 'text-green-700 hover:text-green-900'
              }`}
            >
              {language === 'es' ? 'Inicio' : 'Home'}
            </Link>
            
            {currentCategories.slice(0, 4).map((category) => (
              <a
                key={category.id}
                href={`/#${category.id}`}
                className={`font-medium transition-colors duration-200 hover:underline underline-offset-4 ${
                  isActiveCategory(category.id) ? 'text-green-900 underline' : 'text-green-700 hover:text-green-900'
                }`}
              >
                {category.name}
              </a>
            ))}
            
            <Link
              to="/blog"
              className={`font-medium transition-colors duration-200 hover:underline underline-offset-4 ${
                isActive('/blog') || location.pathname.startsWith('/blog/') ? 'text-green-900 underline' : 'text-green-700 hover:text-green-900'
              }`}
            >
              {t('blog')}
            </Link>
          </nav>

          {/* Search and Language */}
          <div className="flex items-center space-x-4">
            {/* Search */}
            <form onSubmit={handleSearch} className="hidden sm:block">
              <div className="relative">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder={t('search')}
                  className="w-64 pl-10 pr-4 py-2 border border-green-200 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white"
                />
                <Search className="absolute left-3 top-2.5 h-5 w-5 text-green-400" />
              </div>
            </form>

            {/* Language Toggle */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-1 px-3 py-2 rounded-lg bg-green-100 hover:bg-green-200 transition-colors duration-200"
            >
              <Globe className="h-4 w-4 text-green-600" />
              <span className="text-sm font-medium text-green-700 uppercase">{language}</span>
            </button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="lg:hidden p-2 rounded-md text-green-700 hover:bg-green-100 transition-colors duration-200"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden border-t border-green-200 bg-white py-4">
            {/* Mobile Search */}
            <form onSubmit={handleSearch} className="mb-4 sm:hidden">
              <div className="relative">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder={t('search')}
                  className="w-full pl-10 pr-4 py-2 border border-green-200 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <Search className="absolute left-3 top-2.5 h-5 w-5 text-green-400" />
              </div>
            </form>

            {/* Mobile Navigation */}
            <nav className="space-y-2">
              <Link
                to="/"
                className={`block px-3 py-2 rounded-md transition-colors duration-200 ${
                  isActive('/') ? 'bg-green-50 text-green-900' : 'text-green-700 hover:bg-green-50'
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {language === 'es' ? 'Inicio' : 'Home'}
              </Link>
              
              {currentCategories.map((category) => (
                <a
                  key={category.id}
                  href={`/#${category.id}`}
                  className="block px-3 py-2 text-green-700 hover:bg-green-50 rounded-md transition-colors duration-200"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {category.name}
                </a>
              ))}
              
              <Link
                to="/blog"
                className={`block px-3 py-2 rounded-md transition-colors duration-200 ${
                  isActive('/blog') || location.pathname.startsWith('/blog/') ? 'bg-green-50 text-green-900' : 'text-green-700 hover:bg-green-50'
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {t('blog')}
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;