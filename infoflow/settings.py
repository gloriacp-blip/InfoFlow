"""
Configuración de Django para InfoFlow - Proyecto de Portafolio

Este archivo contiene la configuración principal de la aplicación Django.
Se utiliza tanto en desarrollo como en producción con variables de entorno.

Autor: Tu Nombre
Fecha: 2024
"""

import os
from pathlib import Path
from decouple import config, Csv

# ============================================================================
# CONFIGURACIÓN BASE
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para producción - DEBE cambiar en deployment
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-change-this-key-in-production'
)

# Modo debug - DEBE ser False en producción
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos para acceder a la aplicación
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv()
)

# ============================================================================
# APLICACIONES INSTALADAS
# ============================================================================

INSTALLED_APPS = [
    # Aplicaciones de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Aplicaciones de terceros
    "corsheaders",
    
    # Aplicaciones locales
    "organizer",
]

# ============================================================================
# MIDDLEWARE
# ============================================================================

MIDDLEWARE = [
    # Seguridad
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Servir archivos estáticos
    
    # Sesiones y CSRF
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    
    # Autenticación y mensajes
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    
    # Seguridad adicional
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ============================================================================
# CONFIGURACIÓN DE URLS Y TEMPLATES
# ============================================================================

ROOT_URLCONF = "infoflow.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "infoflow.wsgi.application"

# ============================================================================
# BASE DE DATOS
# ============================================================================

# Configuración de PostgreSQL para producción
DATABASES = {
    "default": {
        "ENGINE": config(
            'DB_ENGINE',
            default='django.db.backends.postgresql'
        ),
        "NAME": config('DB_NAME', default='infoflow_db'),
        "USER": config('DB_USER', default='postgres'),
        "PASSWORD": config('DB_PASSWORD', default=''),
        "HOST": config('DB_HOST', default='localhost'),
        "PORT": config('DB_PORT', default='5432'),
    }
}

# ============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ============================================================================
# INTERNACIONALIZACIÓN
# ============================================================================

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ============================================================================
# ARCHIVOS ESTÁTICOS
# ============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Para producción
STATICFILES_DIRS = [BASE_DIR / "static"]

# Optimización de archivos estáticos en producción
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================================================================
# CONFIGURACIÓN DE MODELOS
# ============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

# CORS - Permitir solicitudes desde dominios específicos
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=Csv()
)

# HTTPS - Requerir HTTPS en producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ============================================================================
# LOGGING
# ============================================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}