# InfoFlow - Organizador de Recursos Digitales

**InfoFlow** es una aplicación web desarrollada con **Python, Django y PostgreSQL** que permite organizar, clasificar y gestionar recursos digitales (enlaces, documentos, referencias) de manera eficiente.

## 🎯 Problema que Resuelve

Cuando una persona o equipo maneja muchos recursos digitales, se vuelve difícil:
- **Encontrar** información relevante rápidamente
- **Clasificar** recursos por temas o categorías
- **Dar seguimiento** al estado de revisión de documentos
- **Priorizar** qué recursos son más importantes

**InfoFlow** centraliza toda esta información en una sola plataforma, permitiendo búsqueda avanzada, filtros inteligentes y un dashboard con estadísticas en tiempo real.

## ✨ Características Principales

### 📊 Dashboard Inteligente
- Estadísticas en tiempo real de recursos
- Resumen de categorías con más contenido
- Búsqueda rápida integrada
- Vista de recursos recientes

### 🏷️ Gestión de Categorías
- Crear, editar y eliminar categorías
- Descripción detallada de cada categoría
- Conteo automático de recursos por categoría
- Slugs amigables para URLs

### 📚 Gestión de Recursos
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Búsqueda por título y descripción
- Filtros por categoría, estado y prioridad
- Estados: Pendiente, Revisado, Importante
- Prioridades: Alta, Media, Baja
- Soporte para URLs/enlaces
- Paginación automática

### 🔍 Búsqueda y Filtros Avanzados
- Búsqueda full-text en título y descripción
- Filtros por categoría
- Filtros por estado
- Combinación de múltiples filtros
- Búsqueda case-insensitive

### 📱 Interfaz Responsiva
- Diseño moderno y limpio
- Compatible con dispositivos móviles
- Tema oscuro profesional
- Navegación intuitiva

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Descripción |
|-----------|---------|------------|
| **Python** | 3.11+ | Lenguaje de programación |
| **Django** | 4.2+ | Framework web |
| **PostgreSQL** | 12+ | Base de datos relacional |
| **HTML5** | - | Estructura de páginas |
| **CSS3** | - | Estilos y diseño responsivo |
| **Gunicorn** | 21.2+ | Servidor WSGI para producción |
| **WhiteNoise** | 6.6+ | Servir archivos estáticos |

## 📋 Requisitos Previos

Antes de instalar InfoFlow, asegúrate de tener:

- **Python 3.11+** instalado
- **PostgreSQL 12+** instalado y ejecutándose
- **pip** (gestor de paquetes de Python)
- **git** (para clonar el repositorio)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/infoflow.git
cd infoflow
```

### 2. Crear un Entorno Virtual

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura tus variables:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DB_NAME=infoflow_db
DB_USER=postgres
DB_PASSWORD=tu-contraseña
DB_HOST=localhost
DB_PORT=5432
```

### 5. Crear la Base de Datos

```bash
# Crear la base de datos en PostgreSQL
createdb infoflow_db

# O usando psql
psql -U postgres -c "CREATE DATABASE infoflow_db;"
```

### 6. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 7. Crear un Superusuario (Admin)

```bash
python manage.py createsuperuser
```

Sigue las indicaciones para crear tu usuario administrador.

### 8. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede a la aplicación en: `http://localhost:8000`

Panel de administración: `http://localhost:8000/admin`

## 📖 Guía de Uso

### Navegación Principal

- **Dashboard**: Página principal con estadísticas y búsqueda rápida
- **Recursos**: Lista completa de todos los recursos
- **Categorías**: Gestión de categorías
- **Admin**: Panel de administración de Django

### Crear una Categoría

1. Ve a **Categorías** → **Nueva categoría**
2. Ingresa el nombre y descripción
3. Haz clic en **Crear**

### Crear un Recurso

1. Ve a **Recursos** → **Nuevo recurso**
2. Completa los campos:
   - **Título**: Nombre descriptivo
   - **Descripción**: Detalles del recurso
   - **URL**: Enlace (opcional)
   - **Categoría**: Selecciona una categoría
   - **Estado**: Pendiente, Revisado o Importante
   - **Prioridad**: Alta, Media o Baja
3. Haz clic en **Crear**

### Buscar y Filtrar

En el **Dashboard** o en **Recursos**:
1. Ingresa un término de búsqueda en el campo de texto
2. Selecciona una categoría (opcional)
3. Selecciona un estado (opcional)
4. Haz clic en **Filtrar** o **Aplicar filtros**

## 🏗️ Estructura del Proyecto

```
infoflow/
├── infoflow/                 # Configuración principal de Django
│   ├── settings.py          # Configuración de la aplicación
│   ├── urls.py              # Rutas principales
│   ├── wsgi.py              # Configuración WSGI
│   └── asgi.py              # Configuración ASGI
├── organizer/               # Aplicación principal
│   ├── models.py            # Modelos de datos (Category, Resource)
│   ├── views.py             # Vistas y lógica de negocio
│   ├── forms.py             # Formularios con validaciones
│   ├── urls.py              # Rutas de la aplicación
│   ├── admin.py             # Configuración del admin
│   └── templates/           # Templates HTML
├── templates/               # Templates base
├── static/                  # Archivos estáticos (CSS, JS)
├── manage.py                # Script de gestión de Django
├── requirements.txt         # Dependencias del proyecto
├── .env.example             # Ejemplo de variables de entorno
└── README.md                # Este archivo
```

## 🔐 Seguridad

### Mejores Prácticas Implementadas

✅ **Validación de Entrada**: Todos los formularios validan datos del usuario
✅ **Protección CSRF**: Tokens CSRF en todos los formularios
✅ **SQL Injection Prevention**: Uso de ORM de Django
✅ **XSS Prevention**: Escapado automático de contenido en templates
✅ **HTTPS Ready**: Configuración para producción con SSL
✅ **Contraseñas Seguras**: Validadores de contraseña configurados
✅ **Secrets Management**: Variables de entorno para datos sensibles

### Configuración de Seguridad en Producción

En `.env` para producción:

```env
DEBUG=False
SECRET_KEY=your-very-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📦 Despliegue en Producción

### Usando Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Crear aplicación
heroku create tu-app-name

# Configurar variables de entorno
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-postgres-url

# Desplegar
git push heroku main

# Ejecutar migraciones
heroku run python manage.py migrate
```

### Usando Docker

```bash
# Construir imagen
docker build -t infoflow .

# Ejecutar contenedor
docker run -p 8000:8000 infoflow
```

### Usando Gunicorn + Nginx

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar aplicación
gunicorn infoflow.wsgi:application --bind 0.0.0.0:8000

# Configurar Nginx como proxy reverso
# (Ver documentación de Nginx)
```

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas de una aplicación específica
python manage.py test organizer

# Ejecutar con cobertura
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Optimizaciones Implementadas

### Base de Datos
- ✅ Índices en campos frecuentemente buscados
- ✅ `select_related()` para evitar N+1 queries
- ✅ `annotate()` para agregaciones eficientes

### Rendimiento
- ✅ Paginación en listas de recursos
- ✅ Caché de archivos estáticos con WhiteNoise
- ✅ Compresión de archivos estáticos

### Código
- ✅ Validaciones en modelos y formularios
- ✅ Decoradores `@require_http_methods` para seguridad
- ✅ Mensajes de usuario con Django Messages Framework
- ✅ Código documentado con docstrings

## 🐛 Solución de Problemas

### Error: "psycopg2 no encontrado"

```bash
pip install psycopg2-binary
```

### Error: "Base de datos no existe"

```bash
createdb infoflow_db
python manage.py migrate
```

### Error: "SECRET_KEY no configurado"

Asegúrate de tener un archivo `.env` con `SECRET_KEY` definido.

### Error: "Archivos estáticos no se cargan"

```bash
python manage.py collectstatic --noinput
```

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes preguntas o encuentras problemas, abre un issue en GitHub o contacta al autor.

---

**Hecho con ❤️ para Google**
