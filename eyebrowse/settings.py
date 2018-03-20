# Django settings for eyebrowse project.
import os
import django

from registration_defaults.settings import *
from django.core.urlresolvers import get_resolver


DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

_ENV_FILE_PATH = '/opt/eyebrowse/env'
_DEBUG_FILE_PATH = '/opt/eyebrowse/debug'


def _get_env():
    f = open(_ENV_FILE_PATH)
    env = f.read()

    if env[-1] == '\n':
        env = env[:-1]

    f.close()
    return env
ENV = _get_env()


def _get_debug():
    f = open(_DEBUG_FILE_PATH)
    debug = f.read()

    if debug[-1] == '\n':
        debug = debug[:-1]

    f.close()
    if debug == 'true':
        return True
    else:
        return False

DEBUG = _get_debug()

try:
    execfile(SITE_ROOT + '/../config.py')
except IOError:
    print "Unable to open configuration file!"

if ENV == 'prod':
    BASE_URL = 'https://pano.csail.mit.edu'
    DB_CONF = DB_CONF_PROD
else:
    BASE_URL = 'http://localhost:8000'
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    AWS["BUCKET"] = AWS["BUCKET_DEV"]
    DB_CONF = DB_CONF_LOCAL

TEMPLATE_DEBUG = DEBUG

# custom auth
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

LOGIN_REDIRECT_URL = "/"
DEFAULT_EMAIL = "eyebrowse@mit.edu"
DEFAULT_FROM_EMAIL = DEFAULT_EMAIL

ADMINS = (
    ('eyebrowse-admins', DEFAULT_EMAIL),
    ('amy', 'axz@mit.edu'),
    ('jessica', 'jzwang@mit.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': DB_CONF["TYPE"],
        'NAME': DB_CONF["NAME"],  # Or path to database file if using sqlite3.
        'USER': DB_CONF["USER"],  # Not used with sqlite3.
        'PASSWORD': DB_CONF["PASSWORD"],  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': DB_CONF["HOST"],
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        'STORAGE_ENGINE': 'MyISAM'
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

AUTHENTICATION_BACKENDS = [
    'eyebrowse.backends.EmailOrUsernameBackend',
]

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',

    'compressor.finders.CompressorFinder',
)

# settings for django-compressor
COMPRESS_CSS_FILTERS = (
    'compressor.filters.template.TemplateFilter',
)

# Make this unique, and don't share it with anybody.
# SECRET_KEY is loaded in by config.py

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'common.middleware.crossdomainxhr.XsSharing',
    'common.middleware.proxy.ProxyMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'common.middleware.profiler.ProfileMiddleware',
)

ROOT_URLCONF = 'eyebrowse.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'eyebrowse.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'registration_defaults',
    'django_admin_bootstrapped',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    # third party
    'compressor',
    'gunicorn',
    'registration',
    'tastypie',
    'kronos',
    'south',
    'notifications',
    'languages',
    'tracking',
    'proofread.contrib.django_proofread',

    # eyebrowse
    'accounts',
    'common',
    'api',
    'live_stream',
    'stats',
    'extension',
    'tags'

)

APPEND_SLASH = False

#notification settings
PINAX_NOTIFICATIONS_LANGUAGE_MODEL = "languages.Language"

def PINAX_NOTIFICATIONS_GET_LANGUAGE_MODEL():
    import languages
    return languages.models.Language

PINAX_NOTIFICATIONS_BACKENDS = [("email", "notifications.backends.email.EmailBackend")]

PINAX_NOTIFICATIONS_QUEUE_ALL = False


# email settings from sendgrid.com
EMAIL_HOST = EMAIL["EMAIL_HOST"]
EMAIL_HOST_USER = EMAIL["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = EMAIL["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = EMAIL["EMAIL_PORT"]
EMAIL_USE_TLS = EMAIL["EMAIL_USE_TLS"]

ACCOUNT_ACTIVATION_DAYS = 14  # Two-week activation window;


# Tastypie settings:
API_LIMIT_PER_PAGE = 0  # no default
TASTYPIE_FULL_DEBUG = DEBUG
TASTYPIE_ALLOW_MISSING_SLASH = True


#django-tracking settings
TRACK_AJAX_REQUESTS = True
TRACK_ANONYMOUS_USERS = True
TRACK_PAGEVIEWS = True
TRACK_REFERER = True
TRACK_QUERY_STRING = True
TRACK_IGNORE_URLS = ['static.*?',
                     'ext/bubbleInfo',
                     'accounts/login',
                     'tracking',
                     'api/v1/whitelist',
                     'api/v1/blacklist',
                     'api/v1/history-data',
                     'tags/initialize_page',
                     'tags/page',
                     'tags/tags/page',
                     'tags/page/related_stories',
                     'tags/page/summary',
                     'tags/user/tags',
                     'tags/highlights',
                     'tags/common_tags',
                     'accounts/logout',
                     'robots.txt']
TRACK_IGNORE_STATUS_CODES = [400, 404, 403, 405, 410, 500]


# gravatar settings
GRAVATAR_IMG_CLASS = "img-polaroid"
# DEFAULT_IMG = "/static/common/img/placeholder.png"


# cross domain sharing
XS_SHARING_ALLOWED_HEADERS = [
    "x-csrftoken",
]

COMPRESS_DEBUG_TOGGLE = None
COMPRESS_ENABLED = not DEBUG
COMPRESS_PRECOMPILERS = ()


def get_proofread_urls(exclusion_patterns=None):
    if exclusion_patterns is None:
        exclusion_patterns = {}

    patterns = []
    for group in get_resolver(None).reverse_dict.itervalues():
        pattern = '/' + group[0][0][0]
        if '%' in pattern:
            continue
        skip = False
        for excluded in exclusion_patterns:
            if excluded in pattern:
                skip = True
                break
        if not skip:
            patterns.append(pattern)


    return patterns

exclusion_patterns = ['/consent', '/getting_started', '/add_tag',
'/accounts/profile/connections', '/accounts/password/change/',
'/consent_accept', '/ext/getFriends', '/notifications/settings/', '/color_tag',
'/password_change/done/', '/notifications', '/password_change/',
'/ext/profilepic', '/accounts/profile/sync_delicious',
'/accounts/profile/edit_tags', '/accounts/profile/whitelist',
'/accounts/connect', '/delete_tag', '/accounts/profile/mutelist',
'/password_change/', '/api/delete_eyehistory', '/notifications/settings/',
'/password_change/done/', '/accounts/profile/sync_twitter', '/ext/getStats',
'/tracking/', '/live_stream/', '/tracking/', '/ext/tickerInfo', '/feedback',
'/ext/bubbleInfo', '/api/mutelist/add/', '/ext/getActiveUsers',
'/accounts/password/change/done/', '/ext/getMessages',
'/accounts/profile/account', '/api/whitelist/add/']

PROOFREAD_SUCCESS = get_proofread_urls(exclusion_patterns=exclusion_patterns)
exclusion_patterns.remove('/ext/profilepic')
PROOFREAD_ENDPOINTS = map(lambda x: (x, 302), exclusion_patterns)



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
