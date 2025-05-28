import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

# Docker properties
# SECRET_KEY = os.environ.get("SECRET_KEY")
# DEBUG = os.environ.get("DEBUG")
# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split()


SECRET_KEY = "django-insecure-s2l-7eu!5s)n50pc&2)ya(-e=tehko1tp*(ol4s-x)8_0jub%*"


# DEBUG = False
DEBUG = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": "logs/debug.log",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#     },
# }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "requests.log",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

REST_TITLE = "EDUSYSTEM API"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "parler",
    "parler_rest",
    "import_export",
    "debug_toolbar",
    "django_filters",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "main.apps.MainConfig",
    "bmdu_api.apps.BmduApiConfig",
    "mmu_api.apps.MmuApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "main.middleware.RequestLoggerMiddleware",
    "main.middleware.DrfTitleMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "server.wsgi.application"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("EDUSYSTEM",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=6),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(hours=12),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "EDUSYSTEM API",
    "DESCRIPTION": "EDUSYSTEM API documentation",
    "VERSION": "1.0.3",
    "SERVE_INCLUDE_SCHEMA": False,
    "REDOC_DIST": "SIDECAR",
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "edusystem",
#         "USER": "neharix",
#         "PASSWORD": "ghost2928",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# For Docker

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_DB"),
#         "USER": os.environ.get("POSTGRES_USER"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#         "HOST": "db",
#         "PORT": 5432,
#     }
# }


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


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + ["x-service"]

CSRF_TRUSTED_ORIGINS = ["https://bmdu.depder.com", "http://localhost:5173"]


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.AllowAny",
    #     # "rest_framework.permissions.IsAuthenticated",
    # ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "500/minute",
    },
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

LANGUAGE_CODE = "tk"

LANGUAGES = (
    ("en", "English"),
    ("ru", "Russian"),
    ("tk", "Turkmen"),
)

PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "ru"},
        {"code": "tk"},
    ),
    "default": {
        "fallback": "tk",
        "hide_untranslated": False,
    },
}

TIME_ZONE = "Asia/Ashgabat"

USE_I18N = True

USE_TZ = True

# STATIC_URL = "static/"
STATIC_URL = "/api/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/api/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
