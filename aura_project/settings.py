"""
Django settings for aura_project — production-ready.
Конфигурация через django-environ (.env файл).
"""
import os
from pathlib import Path

import environ

# ─────────────────────────────────────────────────────────────────────────────
# BASE PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["127.0.0.1"]),
    DB_ENGINE=(str, "django.db.backends.sqlite3"),
    TIME_ZONE=(str, "Asia/Bishkek"),
)

# Читаем .env из корня проекта (если существует)
environ.Env.read_env(BASE_DIR / ".env")

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# HTTPS security headers (активируются только в production)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000        # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Домены, с которых принимаются CSRF-запросы (для DRF и форм)
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["https://menu.barca.kg"],
)
WHITENOISE_MANIFEST_STRICT = False
X_FRAME_OPTIONS = "DENY"

# ─────────────────────────────────────────────────────────────────────────────
# APPLICATIONS
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # REST Framework
    "rest_framework",

    # Локальные приложения
    "menu.apps.MenuConfig",
]

# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise сразу после SecurityMiddleware — обрабатывает статику до Django
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "aura_project.urls"

# ─────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────
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

WSGI_APPLICATION = "aura_project.wsgi.application"

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────────────────────
_db_engine = env("DB_ENGINE")

if _db_engine == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": _db_engine,
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST", default="aura-db"),
            "PORT": env("DB_PORT", default="5432"),
            "CONN_MAX_AGE": 60,             # persistent connections
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }

# ─────────────────────────────────────────────────────────────────────────────
# CACHE (Redis)
# ─────────────────────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://aura-redis:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": True,      # сервер не падает при недоступности Redis
        },
        "KEY_PREFIX": "aura",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ─────────────────────────────────────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = "ru"
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("ru", "Русский"),
    ("en", "English"),
    ("ky", "Кыргызча"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# ─────────────────────────────────────────────────────────────────────────────
# STATIC FILES (WhiteNoise)
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL = env("STATIC_URL", default="/static/")
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise: Brotli/Gzip сжатие + иммутабельный кэш для хэшированных файлов
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Браузер кэширует статику 1 год (работает с ManifestStaticFilesStorage)
WHITENOISE_MAX_AGE = 31536000

# ─────────────────────────────────────────────────────────────────────────────
# MEDIA FILES
# ─────────────────────────────────────────────────────────────────────────────
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = BASE_DIR / "media"

# ─────────────────────────────────────────────────────────────────────────────
# REST FRAMEWORK
# ─────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "120/minute",
        "user": "300/minute",
    },
    # Пагинация по умолчанию
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}

# CORS: разрешаем запросы с поддомена menu.barca.kg
# Установите django-cors-headers если нужен браузерный cross-origin доступ:
#   pip install django-cors-headers
# CORS_ALLOWED_ORIGINS = ["https://menu.barca.kg"]

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING (ротация файлов — не забьёт диск)
# ─────────────────────────────────────────────────────────────────────────────
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING — только консоль (чтобы контейнер не падал)
# ─────────────────────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "menu": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT PRIMARY KEY FIELD TYPE
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────────────────────────────────────────────────────────────────────────
# JAZZMIN — оформление Django Admin
# ─────────────────────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "AURA Admin",
    "site_header": "AURA Fine Dining",
    "site_brand": "✦ AURA",
    "welcome_sign": "Добро пожаловать в панель управления",
    "copyright": "AURA Fine Dining",

    "search_model": ["menu.Dish", "menu.Category"],
    "user_avatar": None,

    "topmenu_links": [
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Открыть сайт", "url": "/", "new_window": True},
    ],

    "usermenu_links": [
        {"name": "Открыть сайт", "url": "/", "icon": "fas fa-globe", "new_window": True},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "order_with_respect_to": [
        "menu",
        "menu.Category",
        "menu.Dish",
        "menu.RestaurantInfo",
        "menu.Greeting",
        "menu.InfoRule",
        "menu.Fine",
        "auth",
    ],

    "custom_links": {
        "menu": [{
            "name": "Открыть меню на сайте",
            "url": "/",
            "icon": "fas fa-external-link-alt",
            "new_window": True,
        }],
    },

    "icons": {
        "auth":                  "fas fa-users-cog",
        "auth.user":             "fas fa-user",
        "auth.Group":            "fas fa-users",
        "menu.category":         "fas fa-th-large",
        "menu.dish":             "fas fa-utensils",
        "menu.ingredient":       "fas fa-leaf",
        "menu.restaurantinfo":   "fas fa-store",
        "menu.greeting":         "fas fa-language",
        "menu.inforule":         "fas fa-clipboard-list",
        "menu.fine":             "fas fa-exclamation-triangle",
        "menu.sociallinks":      "fas fa-share-alt",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,

    "changeform_format": "horizontal_tabs",
    "changeform_format_override": {
        "auth.user": "collapsible",
    },
    "language_chooser": False,

    "custom_css": "admin/css/aura_admin.css",
}

JAZZMIN_UI_TWEAKS = {}
