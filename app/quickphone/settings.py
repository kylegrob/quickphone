"""Settings for the Quick Phone Repair Management System (Sprint 4 training build).

Architecture follows the Sprint 3 Alternative Matrix and Hardware-Software
Specification: Django 5.2, one PostgreSQL database for both stores.
Configuration comes from environment variables so no secret lives in the repo.
"""
import os
import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Fail closed: debug is off unless QP_DEBUG=1 is set, and with debug off the app refuses to
# start without its own secret and passcode keys (security analysis F1, 2026-11-06). The fallback
# key below is public (it is in this repository) and is accepted only for local training and tests.
DEBUG = os.environ.get("QP_DEBUG", "0") == "1"
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
DEV_FALLBACK_ALLOWED = DEBUG or TESTING
SECRET_KEY = os.environ.get("QP_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEV_FALLBACK_ALLOWED:
        raise ImproperlyConfigured("Set QP_SECRET_KEY (50+ random characters), or QP_DEBUG=1 on a training machine.")
    SECRET_KEY = "dev-only-not-for-deployment-quickphone-training"
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
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
     "OPTIONS": {"user_attributes": ("email", "first_name", "last_name")}},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Sign-in lockout (F4): after this many failed attempts for one email address, that account
# cannot sign in for LOGIN_LOCK_MINUTES. Counted per account, not per address, because both
# stores share one internet connection.
LOGIN_MAX_FAILURES = int(os.environ.get("QP_LOGIN_MAX_FAILURES", "5"))
LOGIN_LOCK_MINUTES = int(os.environ.get("QP_LOGIN_LOCK_MINUTES", "15"))

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

# Device passcodes are encrypted at rest (owner, Oct 23 #7). With debug off QP_PASSCODE_KEY (a Fernet
# key) is required; only training and tests fall back to a key derived from SECRET_KEY (F1).
# Generate one with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
PASSCODE_KEY = os.environ.get("QP_PASSCODE_KEY", "")
if not PASSCODE_KEY and not DEV_FALLBACK_ALLOWED:
    raise ImproperlyConfigured("Set QP_PASSCODE_KEY to a Fernet key, or QP_DEBUG=1 on a training machine.")

# Appointment slots (FR01). Store hours are not yet confirmed by the owner;
# these values are placeholders to confirm.
APPOINTMENT_FIRST_SLOT = "09:00"
APPOINTMENT_LAST_SLOT = "17:00"
APPOINTMENT_SLOT_MINUTES = 30
APPOINTMENT_DAYS_AHEAD = 7

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# Counter computers are shared (F3): a session ends after QP_SESSION_MINUTES without activity
# and when the browser closes.
SESSION_COOKIE_AGE = int(os.environ.get("QP_SESSION_MINUTES", "30")) * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# HTTPS (F2). With debug off, cookies travel only over HTTPS and plain HTTP is redirected.
# HSTS starts at 30 days; raise it once HTTPS is known to work on both stores' machines.
# Set QP_BEHIND_PROXY=1 only when a reverse proxy terminates HTTPS and sets X-Forwarded-Proto.
# The test client speaks plain HTTP, so tests check these settings in a separate process.
if not DEBUG and not TESTING:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = os.environ.get("QP_SSL_REDIRECT", "1") == "1"
    SECURE_HSTS_SECONDS = int(os.environ.get("QP_HSTS_SECONDS", str(30 * 24 * 3600)))
    if os.environ.get("QP_BEHIND_PROXY") == "1":
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
