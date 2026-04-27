"""
Django settings for aura_project.
"""
from pathlib import Path
from decouple import config, Csv

# ============================================================
# BASE PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SECURITY
# ============================================================
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())

# ============================================================
# APPLICATIONS
# ============================================================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Локальные приложения
    'menu.apps.MenuConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aura_project.urls'

# ============================================================
# TEMPLATES
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aura_project.wsgi.application'

# ============================================================
# DATABASE
# ============================================================
_db_engine = config('DB_ENGINE', default='django.db.backends.sqlite3')

if _db_engine == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': _db_engine,
            'NAME':     config('DB_NAME'),
            'USER':     config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST':     config('DB_HOST', default='localhost'),
            'PORT':     config('DB_PORT', default='5432'),
        }
    }

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'ru'
TIME_ZONE = config('TIME_ZONE', default='Asia/Bishkek')
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('ky', 'Кыргызча'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ============================================================
# STATIC FILES
# ============================================================
STATIC_URL = config('STATIC_URL', default='/static/')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============================================================
# MEDIA FILES
# ============================================================
MEDIA_URL  = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# JAZZMIN — оформление Django Admin
# ============================================================
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
