import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useCategories = (language = 'es') => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const data = await apiService.getCategories(language);
        setCategories(data);
      } catch (err) {
        console.error('Error fetching categories:', err);
        setError('Error al cargar categorías');
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, [language]);

  return { categories, loading, error };
};