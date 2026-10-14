"""
Django settings for config project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Render ma Environment variable ma SECRET_KEY set karjo. Local mate fallback chhe.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-me-locally-only",
)

# Render ma Environment variable DEBUG=False set karjo.
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "essentials-availity.onrender.com",
    "localhost",
    "127.0.0.1",
]


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "accounts",
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

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------
# CORS
# ---------------------------------------------------------------
# TEST mate: badha origin allow. Login chali jaay pachi aa line kadhi
# nakho ane niche ni CORS_ALLOWED_ORIGINS vali list active karo.
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "https://essentials-availityyy-com.netlify.app",
#     "http://127.0.0.1:5500",
#     "http://localhost:5500",
#     "http://127.0.0.1:5501",
#     "http://localhost:5501",
# ]

CSRF_TRUSTED_ORIGINS = [
    "https://essentials-availity-com.netlify.app",
    "https://essentials-availity.onrender.com",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]

# Debug: Render Logs ma aa lines dekhavi joiye
print("SETTINGS LOADED:", __file__, flush=True)
print("CORS_ALLOW_ALL_ORIGINS:", CORS_ALLOW_ALL_ORIGINS, flush=True)


# ---------------------------------------------------------------
# Static files
# ---------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# ---------------------------------------------------------------
# Jazzmin (ek j JAZZMIN_SETTINGS, custom_css andar merge karyu chhe)
# ---------------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "All Music Admin",
    "site_header": "All Music",
    "site_brand": "All Music",
    "welcome_sign": "Welcome to All Music Admin",
    "copyright": "All Music",

    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_models": [],
    "hide_apps": [],

    "order_with_respect_to": [
        "accounts",
        "auth",
    ],

    "icons": {
        "accounts.Device": "fas fa-mobile-alt",
        "auth.User": "fas fa-users",
        "auth.Group": "fas fa-user-shield",
    },

    "custom_links": {
        "accounts": [
            {
                "name": "Device Approvals",
                "url": "admin:accounts_device_changelist",
                "icon": "fas fa-check-circle",
            },
        ],
    },

    "topmenu_links": [
        {
            "name": "Dashboard",
            "url": "admin:index",
            "permissions": ["auth.view_user"],
        },
        {
            "name": "Users",
            "url": "admin:auth_user_changelist",
            "permissions": ["auth.view_user"],
        },
        {
            "name": "Devices",
            "url": "admin:accounts_device_changelist",
            "permissions": ["accounts.view_device"],
        },
    ],

    "usermenu_links": [
        {
            "name": "All Music Website",
            "url": "https://essentials-availity-com.netlify.app/",
            "new_window": True,
        },
    ],

    "related_modal_active": True,
    "show_ui_builder": True,

    "custom_css": "admin/css/custom.css",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "default",
    "default_theme_mode": "light",

    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    "brand_colour": "navbar-dark",
    "accent": "accent-primary",

    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,

    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_flat_style": False,
    "sidebar_nav_legacy_style": False,

    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}