import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useArticles = (category = null, language = 'es') => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const params = { language };
        if (category && category !== 'all') params.category = category;
        
        const data = await apiService.getArticles(params);
        setArticles(data);
      } catch (err) {
        console.error('Error fetching articles:', err);
        setError('Error al cargar artículos');
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, [category, language]);

  return { articles, loading, error };
};

export const useArticle = (slug, language = 'es') => {
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticle = async () => {
      if (!slug) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const data = await apiService.getArticleBySlug(slug, language);
        setArticle(data);
      } catch (err) {
        console.error('Error fetching article:', err);
        setError('Error al cargar artículo');
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [slug, language]);

  return { article, loading, error };
};

export const useRelatedArticles = (articleId, language = 'es') => {
  const [relatedArticles, setRelatedArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRelatedArticles = async () => {
      if (!articleId) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const data = await apiService.getRelatedArticles(articleId, language);
        setRelatedArticles(data);
      } catch (err) {
        console.error('Error fetching related articles:', err);
        setError('Error al cargar artículos relacionados');
      } finally {
        setLoading(false);
      }
    };

    fetchRelatedArticles();
  }, [articleId, language]);

  return { relatedArticles, loading, error };
};