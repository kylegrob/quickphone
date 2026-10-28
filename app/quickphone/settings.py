"""Settings for the Quick Phone Repair Management System (Sprint 4 training build).

Architecture follows the Sprint 3 Alternative Matrix and Hardware-Software
Specification: Django 5.2, one PostgreSQL database for both stores.
Configuration comes from environment variables so no secret lives in the repo.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# A development-only key is used when QP_SECRET_KEY is unset. Never deploy with it.
SECRET_KEY = os.environ.get("QP_SECRET_KEY", "dev-only-not-for-deployment-quickphone-training")
DEBUG = os.environ.get("QP_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("QP_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]").split(",")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "shop.permissions.ActiveStoreMiddleware",
]

ROOT_URLCONF = "quickphone.urls"

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
                "shop.permissions.nav_context",
            ],
        },
    },
]

WSGI_APPLICATION = "quickphone.wsgi.application"

# PostgreSQL is the database of record (Sprint 3 specification). QP_DB_ENGINE=sqlite
# exists only so the automated tests can run on a machine without PostgreSQL.
if os.environ.get("QP_DB_ENGINE", "postgresql") == "sqlite":
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "dev.sqlite3"}}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("QP_DB_NAME", "quickphone"),
            "USER": os.environ.get("QP_DB_USER", "quickphone"),
            "PASSWORD": os.environ.get("QP_DB_PASSWORD", ""),
            "HOST": os.environ.get("QP_DB_HOST", "localhost"),
            "PORT": os.environ.get("QP_DB_PORT", "5432"),
        }
    }

AUTH_USER_MODEL = "shop.Employee"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = False
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Pickup notifications (FR12). In training, emails are written to files in
# sent_emails/ instead of being delivered; deployment sets the store's SMTP account.
EMAIL_BACKEND = os.environ.get("QP_EMAIL_BACKEND", "django.core.mail.backends.filebased.EmailBackend")
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
EMAIL_HOST = os.environ.get("QP_EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("QP_EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("QP_EMAIL_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("QP_EMAIL_PASSWORD", "")
EMAIL_USE_TLS = True

# Device passcodes are encrypted at rest (owner, Oct 23 #7). Deployment must set
# QP_PASSCODE_KEY (a Fernet key); otherwise a key is derived from SECRET_KEY.
PASSCODE_KEY = os.environ.get("QP_PASSCODE_KEY", "")

# Appointment slots (FR01). Store hours are not yet confirmed by the owner;
# these values are placeholders to confirm.
APPOINTMENT_FIRST_SLOT = "09:00"
APPOINTMENT_LAST_SLOT = "17:00"
APPOINTMENT_SLOT_MINUTES = 30
APPOINTMENT_DAYS_AHEAD = 7

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
