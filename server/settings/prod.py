from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]


ADMINS = [
    ("skill", "g@g.com"),
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
