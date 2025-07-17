# BambuGoods - Backend API Contracts

## Resumen del Backend

El backend de BambuGoods manejará:
- **Gestión de productos eco-sostenibles** con información completa (nombre, descripción, precio, imágenes, etc.)
- **Sistema de categorías** para organizar productos
- **Gestión de favoritos por usuario** (usando localStorage como identificador simple)
- **Búsqueda y filtrado** de productos
- **Soporte multiidioma** en la base de datos

## Modelos de Datos (MongoDB)

### 1. Product Model
```javascript
{
  _id: ObjectId,
  name: {
    es: String, // "Cepillo de Dientes de Bambú Adulto"
    en: String  // "Adult Bamboo Toothbrush"
  },
  description: {
    es: String,
    en: String
  },
  category: String, // "cepillos-bambu", "champu-solido", etc.
  price: Number, // 8.99
  originalPrice: Number, // 12.99
  image: String, // URL de la imagen
  amazonLink: String, // Link de afiliado
  rating: Number, // 4.5
  reviews: Number, // 234
  features: {
    es: [String], // ["100% bambú sostenible", "Cerdas libres de BPA"]
    en: [String]  // ["100% sustainable bamboo", "BPA-free bristles"]
  },
  isActive: Boolean, // true
  createdAt: Date,
  updatedAt: Date
}
```

### 2. Category Model
```javascript
{
  _id: ObjectId,
  id: String, // "cepillos-bambu"
  name: {
    es: String, // "Cepillos de Bambú"
    en: String  // "Bamboo Brushes"
  },
  icon: String, // "Brush"
  isActive: Boolean,
  createdAt: Date
}
```

### 3. UserFavorite Model
```javascript
{
  _id: ObjectId,
  userId: String, // localStorage ID o IP como identificador simple
  productId: ObjectId, // referencia al producto
  createdAt: Date
}
```

## Endpoints de API

### Productos
- `GET /api/products` - Obtener todos los productos
  - Query params: `?category=cepillos-bambu&language=es&search=bambú`
  - Response: Array de productos con traducción según idioma

- `GET /api/products/:id` - Obtener producto específico
  - Response: Producto con todas las traducciones

- `POST /api/products` - Crear nuevo producto (admin)
- `PUT /api/products/:id` - Actualizar producto (admin)
- `DELETE /api/products/:id` - Eliminar producto (admin)

### Categorías
- `GET /api/categories` - Obtener todas las categorías
  - Query params: `?language=es`
  - Response: Array de categorías traducidas

### Favoritos
- `GET /api/favorites/:userId` - Obtener favoritos del usuario
- `POST /api/favorites` - Agregar producto a favoritos
  - Body: `{userId: string, productId: string}`
- `DELETE /api/favorites/:userId/:productId` - Quitar de favoritos

### Búsqueda
- `GET /api/search` - Búsqueda de productos
  - Query params: `?q=bambú&language=es&category=cepillos-bambu`

## Datos Mock a Migrar

Los datos del archivo `mock.js` incluyen:
- 6 productos base con traducciones completas
- 6 categorías con iconos
- Sistema de traducciones para UI

## Integración Frontend-Backend

### Cambios en Frontend:
1. **Reemplazar mock.js** con llamadas reales a API
2. **Actualizar hooks** para manejar loading states
3. **Gestión de errores** para failed requests
4. **Paginación** para grandes volúmenes de productos

### Archivos a Modificar:
- `HomePage.js` - Reemplazar datos mock con API calls
- `LanguageContext.js` - Mantener traducciones UI, productos vendrán del backend
- Crear `hooks/useProducts.js` - Custom hook para gestión de productos
- Crear `hooks/useFavorites.js` - Custom hook para favoritos
- Crear `services/api.js` - Servicio centralizado para API calls

## Características del Backend

### Funcionalidades Principales:
1. **CRUD completo** para productos y categorías
2. **Filtrado avanzado** por categoría, precio, rating
3. **Búsqueda full-text** en múltiples idiomas
4. **Sistema de favoritos** persistente
5. **Validación de datos** con Pydantic
6. **Manejo de errores** consistente
7. **Logging** para debugging
8. **Paginación** para performance

### Tecnologías:
- **FastAPI** - Framework web moderno
- **MongoDB** - Base de datos NoSQL para flexibilidad
- **Motor** - Driver asíncrono para MongoDB
- **Pydantic** - Validación de datos
- **CORS** - Habilitado para frontend

## Próximos Pasos

1. **Implementar modelos** MongoDB con Motor
2. **Crear endpoints** básicos (GET, POST, PUT, DELETE)
3. **Poblar base de datos** con datos mock
4. **Implementar filtros** y búsqueda
5. **Integrar frontend** con backend
6. **Testing** de endpoints
7. **Optimización** de queries

Este backend proporcionará una base sólida para BambuGoods, permitiendo gestión completa de productos eco-sostenibles con soporte multiidioma y funcionalidades avanzadas de e-commerce.