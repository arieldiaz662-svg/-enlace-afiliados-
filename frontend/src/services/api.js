import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    return Promise.reject(error);
  }
);

// API service methods
export const apiService = {
  // Products
  async getProducts(params = {}) {
    const response = await api.get('/products', { params });
    return response.data;
  },

  async getProductById(id) {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  async searchProducts(params = {}) {
    const response = await api.get('/search', { params });
    return response.data;
  },

  // Categories
  async getCategories(language = 'es') {
    const response = await api.get('/categories', { params: { language } });
    return response.data;
  },

  // Favorites
  async getFavorites(userId) {
    const response = await api.get(`/favorites/${userId}`);
    return response.data;
  },

  async addFavorite(userId, productId) {
    const response = await api.post('/favorites', { userId, productId });
    return response.data;
  },

  async removeFavorite(userId, productId) {
    const response = await api.delete(`/favorites/${userId}/${productId}`);
    return response.data;
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/');
    return response.data;
  }
};

export default api;