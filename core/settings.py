"""
Django settings for core project.

Generated by 'django-store_admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool, True)

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    "https://art-store-production.up.railway.app",
    "https://lumiere.fuzzydevs.com",
    # "http://localhost",
]
# for django debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]
# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "accounts",
    "orders",
    "store",
    "payment",
    # 3rd party
    "crispy_forms",
    "crispy_tailwind",
    "taggit",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates/"],
        # "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("PGHOST"),
        "PORT": env("PGPORT"),
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.User"
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
BAG_SESSION_ID = "bag"
TAGGIT_CASE_INSENSITIVE = True

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGOUT_URL = "accounts:logout"
LOGIN_URL = "accounts:sign_in"
RAZORPAY_ID = env("RAZORPAY_ID")
RAZORPAY_SECRET_KEY = env("RAZORPAY_SECRET_KEY")


AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", str, "eu-north-1")


# Private Media File Storage
AWS_QUERYSTRING_AUTH = False  # Enables signed URLs
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_LOCATION = "static"
MEDIAFILES_LOCATION = "media"

# STATIC_ROOT = "/static/"
MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "media/"
STATIC_URL = "static/"
if DEBUG:
    # Development: use local file system for both default and staticfiles
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    # Production: use S3 for both default and staticfiles
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
        "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
    }

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Lumiere Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Store",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Lumiere",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "/assets/Lumiere.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Lumiere Admin Panel",
    # Copyright on the footer
    "copyright": "Lumiere Store",
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    # "search_model": ["auth.User", "auth.Group"],
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    # "topmenu_links": [
    #     # Url that gets reversed (Permissions can be added)
    #     {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    #     # external url that opens in a new window (Permissions can be added)
    #     {
    #         "name": "Support",
    #         "url": "https://github.com/farridav/django-jazzmin/issues",
    #         "new_window": True,
    #     },
    #     # model admin to link to (Permissions checked against model)
    #     {"model": "auth.User"},
    #     # App with dropdown menu to all its models pages (Permissions checked against models)
    #     {"app": "books"},
    # ],
    # #############
    # # User Menu #
    # #############
    # # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {
    #         "name": "Support",
    #         "url": "https://github.com/farridav/django-jazzmin/issues",
    #         "new_window": True,
    #     },
    #     {"model": "auth.user"},
    # ],
    # #############
    # # Side Menu #
    # #############
    # # Whether to display the side menu
    # "show_sidebar": True,
    # # Whether to aut expand the menu
    # "navigation_expanded": True,
    # # Hide these apps when generating side menu e.g (auth)
    # "hide_apps": [],
    # # Hide these models when generating side menu (e.g auth.user)
    # "hide_models": [],
    # # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
    # # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "books": [
    #         {
    #             "name": "Make Messages",
    #             "url": "make_messages",
    #             "icon": "fas fa-comments",
    #             "permissions": ["books.view_book"],
    #         }
    #     ]
    # },
    # # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # # for the full list of 5.13.0 free icon classes
    # "icons": {
    #     "auth": "fas fa-users-cog",
    #     "auth.user": "fas fa-user",
    #     "auth.Group": "fas fa-users",
    # },
    # # Icons that are used when one is not manually specified
    # "default_icon_parents": "fas fa-chevron-circle-right",
    # "default_icon_children": "fas fa-circle",
    # #################
    # # Related Modal #
    # #################
    # # Use modals instead of popups
    # "related_modal_active": False,
    # #############
    # # UI Tweaks #
    # #############
    # # Relative paths to custom CSS/JS scripts (must be present in static files)
    # "custom_css": None,
    # "custom_js": None,
    # # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    # "use_google_fonts_cdn": True,
    # # Whether to show the UI customizer on the sidebar
    # "show_ui_builder": False,
    # ###############
    # # Change view #
    # ###############
    # # Render out the change view as a single form, or in tabs, current options are
    # # - single
    # # - horizontal_tabs (default)
    # # - vertical_tabs
    # # - collapsible
    # # - carousel
    # "changeform_format": "horizontal_tabs",
    # # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {
    #     "auth.user": "collapsible",
    #     "auth.group": "vertical_tabs",
    # },
    # Add a language dropdown into the admin
    # "language_chooser": True,
}
