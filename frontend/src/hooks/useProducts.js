import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useProducts = (category = null, language = 'es', search = null) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const params = { language };
        if (category && category !== 'all') params.category = category;
        if (search) params.search = search;
        
        const data = await apiService.getProducts(params);
        setProducts(data);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Error al cargar productos');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [category, language, search]);

  return { products, loading, error, refetch: () => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const params = { language };
        if (category && category !== 'all') params.category = category;
        if (search) params.search = search;
        
        const data = await apiService.getProducts(params);
        setProducts(data);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Error al cargar productos');
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }};
};

export const useProduct = (productId) => {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      if (!productId) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const data = await apiService.getProductById(productId);
        setProduct(data);
      } catch (err) {
        console.error('Error fetching product:', err);
        setError('Error al cargar producto');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  return { product, loading, error };
};

export const useSearch = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = async (query, language = 'es', category = null) => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const params = { q: query, language };
      if (category && category !== 'all') params.category = category;
      
      const data = await apiService.searchProducts(params);
      setResults(data);
    } catch (err) {
      console.error('Error searching products:', err);
      setError('Error en la búsqueda');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return { results, loading, error, search };
};