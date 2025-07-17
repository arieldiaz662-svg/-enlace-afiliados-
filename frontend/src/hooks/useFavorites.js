import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';

// Generate a simple user ID based on browser fingerprint
const generateUserId = () => {
  let userId = localStorage.getItem('bambugoods-user-id');
  if (!userId) {
    userId = 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    localStorage.setItem('bambugoods-user-id', userId);
  }
  return userId;
};

export const useFavorites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const userId = generateUserId();

  const fetchFavorites = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await apiService.getFavorites(userId);
      setFavorites(data.favorites || []);
    } catch (err) {
      console.error('Error fetching favorites:', err);
      setError('Error al cargar favoritos');
      setFavorites([]);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchFavorites();
  }, [fetchFavorites]);

  const addFavorite = async (productId) => {
    try {
      await apiService.addFavorite(userId, productId);
      setFavorites(prev => [...prev, productId]);
    } catch (err) {
      console.error('Error adding favorite:', err);
      throw new Error('Error al agregar a favoritos');
    }
  };

  const removeFavorite = async (productId) => {
    try {
      await apiService.removeFavorite(userId, productId);
      setFavorites(prev => prev.filter(id => id !== productId));
    } catch (err) {
      console.error('Error removing favorite:', err);
      throw new Error('Error al quitar de favoritos');
    }
  };

  const toggleFavorite = async (productId) => {
    const isFavorite = favorites.includes(productId);
    
    if (isFavorite) {
      await removeFavorite(productId);
    } else {
      await addFavorite(productId);
    }
  };

  const isFavorite = (productId) => favorites.includes(productId);

  return {
    favorites,
    loading,
    error,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    isFavorite,
    refetch: fetchFavorites
  };
};