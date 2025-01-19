"""
Django settings for gutenberg_api project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-remg5$azdu9==9#1gmihp@rzft^j*1-dewbo&+-=y#)c^zjpfy"

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-remg5$azdu9==9#1gmihp@rzft^j*1-dewbo&+-=y#)c^zjpfy')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS = []

# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
# CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://*.railway.app').split(',')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'corsheaders',
    'books',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    

]

ROOT_URLCONF = "gutenberg_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'books', 'templates'),],
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

WSGI_APPLICATION = "gutenberg_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# # Determine if we're on Railway
# IS_RAILWAY = os.getenv('RAILWAY_ENVIRONMENT') is not None

# # Debug setting
# DEBUG = not IS_RAILWAY  # True locally, False on Railway

# # Hosts settings
# if IS_RAILWAY:
#     ALLOWED_HOSTS = ['.railway.app']
#     CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']
# else:
#     ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
#     CSRF_TRUSTED_ORIGINS = []


IS_RAILWAY = os.getenv('RAILWAY_ENVIRONMENT') is not None

# Database configuration
if IS_RAILWAY:
    # Railway PostgreSQL database
    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    # Local database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'gutenberg'),
            'USER': os.getenv('DB_USER', 'gutenberg'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'gutenberg'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# Determine if we're on Railway
IS_RAILWAY = os.getenv('RAILWAY_ENVIRONMENT') is not None

# Environment settings
if IS_RAILWAY:
    # Railway (Production) settings
    DEBUG = False
    ALLOWED_HOSTS = ['.railway.app']
    CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']
    CORS_ALLOWED_ORIGINS = ['*']
    
    # Security settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Local development settings
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = []
    CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
    
    # Disable security redirects locally
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}