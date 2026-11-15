"""
Django settings for the AlienR portfolio (works locally and on Vercel).

Environment variables (set them in Vercel -> Project -> Settings -> Environment Variables):
  DATABASE_URL          postgres://... (required on Vercel; local falls back to SQLite)
  DJANGO_SECRET_KEY     long random string (strongly recommended)
  DJANGO_DEBUG          "1" only for local debugging (default: off on Vercel, on locally)
  ALLOWED_HOSTS         optional, comma separated extra hosts / custom domains
  SITE_URL              public URL, e.g. https://yourdomain.com (used for canonical/OG tags)
  CLOUDINARY_URL        cloudinary://key:secret@cloud  (needed for image uploads on Vercel)
  EMAIL_HOST_USER / EMAIL_HOST_PASSWORD   Gmail address + app password
  CONTACT_RECIPIENT     where contact/subscribe notifications go
  PORTFOLIO_LINKEDIN_URL  optional LinkedIn profile URL
"""
import hashlib
import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name):
    return [x.strip() for x in os.environ.get(name, "").split(",") if x.strip()]


ON_VERCEL = bool(os.environ.get("VERCEL"))
DEBUG = env_bool("DJANGO_DEBUG", default=not ON_VERCEL)

# --- Database -----------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# --- Secret key ---------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production"
    elif DATABASE_URL:
        # Stable and private (derived from the secret DB URL) so the site keeps
        # working until you add DJANGO_SECRET_KEY. Please set a real one.
        SECRET_KEY = hashlib.sha256(("rocky-secret:" + DATABASE_URL).encode()).hexdigest()
    else:
        raise ImproperlyConfigured("Set DJANGO_SECRET_KEY (and DATABASE_URL) in the environment.")

# --- Hosts / CSRF / HTTPS -----------------------------------------------------
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".vercel.app"] + env_list("ALLOWED_HOSTS")
for _name in ("VERCEL_URL", "VERCEL_BRANCH_URL", "VERCEL_PROJECT_PRODUCTION_URL"):
    _host = os.environ.get(_name, "").strip()
    if _host and _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
for _host in env_list("ALLOWED_HOSTS"):
    if _host.startswith("."):
        CSRF_TRUSTED_ORIGINS.append("https://*" + _host)
    else:
        CSRF_TRUSTED_ORIGINS.append("https://" + _host)

if not DEBUG:
    # Vercel terminates TLS in front of Django; without this, CSRF/redirects misbehave.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- Apps / middleware --------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "web",
]

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

ROOT_URLCONF = "rocky.urls"
WSGI_APPLICATION = "rocky.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "Templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "web.context_processors.site",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- Database -----------------------------------------------------------------
if DATABASE_URL:
    _local_db = any(h in DATABASE_URL for h in ("@localhost", "@127.0.0.1"))
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            # Serverless functions should not hold connections open between requests.
            conn_max_age=int(os.environ.get("DB_CONN_MAX_AGE", "0")),
            conn_health_checks=True,
            ssl_require=not _local_db,
        )
    }
elif DEBUG:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
else:
    raise ImproperlyConfigured("DATABASE_URL is missing. Add your Postgres URL in Vercel's environment variables.")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Static files -------------------------------------------------------------
# Vercel has no build step for Django, so WhiteNoise serves straight from the
# source folders (static/ and the admin's own files): no collectstatic needed.
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG

# --- Media (uploaded project screenshots) -------------------------------------
# Vercel's filesystem is read-only, so uploads go to Cloudinary when configured.
# Files already committed under media/ keep being served from the repo.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
CLOUDINARY_ENABLED = bool(os.environ.get("CLOUDINARY_URL"))
STORAGES = {
    "default": {
        "BACKEND": "web.storage.CloudinaryMediaStorage" if CLOUDINARY_ENABLED
        else "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# --- Email --------------------------------------------------------------------
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # logs instead of failing
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 10  # never let a slow SMTP server hang the serverless function
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or "AlienR <noreply@localhost>"
CONTACT_RECIPIENT = os.environ.get("CONTACT_RECIPIENT", "rockytim5205@gmail.com")
SITE_URL = os.environ.get("SITE_URL", "https://oluwatimilehinagbaje.vercel.app").rstrip("/")

# --- Auth ---------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"

# --- Logging (shows up in Vercel's function logs) ------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
