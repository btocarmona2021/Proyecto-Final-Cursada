from pathlib import Path
import os
from datetime import timedelta  # ← AGREGAR ESTE IMPORT

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-vrf+t%s(@p0+@phoizqxav&s__u91c$_&5kw%gf9%6*j)1bqb-"


DEBUG = os.environ.get("DEBUG", "0") == "1"


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # ← AGREGAR (opcional pero recomendado)
    "corsheaders",
    "core",
    "usuarios.apps.UsuariosConfig",
    "clinica",
    "mascotas",
    "agenda",
    "historia_clinica",
    "internaciones",
    "notificaciones",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "veterinaria.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "veterinaria.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "veterinaria_db2"),
        "USER": os.environ.get("DB_USER", "postgres_user2"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres_pass2"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


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


LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}


# ← AGREGAR ESTA CONFIGURACIÓN COMPLETA DE SIMPLE_JWT
SIMPLE_JWT = {
    # Duración de tokens
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),  # Token de acceso válido por 1 hora
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh token válido por 7 días
    # Rotación de refresh tokens (opcional pero seguro)
    "ROTATE_REFRESH_TOKENS": True,  # Genera nuevo refresh token al refrescar
    "BLACKLIST_AFTER_ROTATION": True,  # Invalida el refresh token anterior
    # Configuración de headers
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # Algoritmo de encriptación
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    # Claims del token
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    # Serializer personalizado (apunta a tu archivo)
    "TOKEN_OBTAIN_SERIALIZER": "usuarios.token_personalizado.CustomTokenObtainPairSerializer",  # ← Ajustar ruta
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://fiery-reece-ecclesiastical.ngrok-free.dev",
]


CORS_ALLOW_CREDENTIALS = True
