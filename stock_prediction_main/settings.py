import os
from pathlib import Path
from datetime import timedelta
import environ

# Path to the root of the Django project (where manage.py and .env live)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environment handler
env = environ.Env()

# Explicitly load .env file
env_file = BASE_DIR / ".env"
environ.Env.read_env(env_file)

# Key variables from .env
SECRET_KEY = env("SECRET_KEY", default="unsafe-default")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])

# Optional: npm for Tailwind build system
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "api",
    "tailwind",
    "theme",
    "django_browser_reload",
    "widget_tweaks",
]
TAILWIND_APP_NAME = "theme"

ROOT_URLCONF = "stock_prediction_main.urls"

# Middleware settings
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Template configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'theme', 'templates')],

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

# Static file settings with WhiteNoise
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# DRF + JWT settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_LIFETIME", default=15)),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_REFRESH_LIFETIME", default=1440)),
}

# Database from .env
DATABASES = {
    "default": env.db(),
}

# Model path for LSTM inference
MODEL_PATH = env("MODEL_PATH", default="stock_prediction_model.keras")

# Auto field config
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
