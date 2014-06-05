# Django settings for eathub project.
from urlparse import urlparse
import os
from django.conf import global_settings
from django.contrib.messages import constants as message_constants

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


if os.getenv('DEBUG', "True") == "True":
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

MONGO_DEFAULT = 'mongodb://127.0.0.1/eathub'
MONGO_URL = urlparse(os.getenv('MONGOHQ_URL', MONGO_DEFAULT))
MONGO_DB = MONGO_URL.path[1:]
MONGO_HOST = MONGO_URL.hostname
MONGO_PORT = MONGO_URL.port
MONGO_USER = MONGO_URL.username
MONGO_PASS = MONGO_URL.password

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': MONGO_DB,
        'USER': MONGO_USER,
        'PASSWORD': MONGO_PASS,
        'HOST': MONGO_HOST,
        'PORT': MONGO_PORT,
        'SUPPORTS_TRANSACTIONS': False,
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

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
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-e-pyb=773m948j0mtj8wx^@^^!-4_@+@nakl!6&-f52v9xiz$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Config needed for sslify app
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'eathub.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'eathub.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(BASE_DIR, '..', 'templates').replace('\\','/')
    os.path.join(BASE_DIR, 'templates').replace('\\', '/')
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'eathub',
    'webapp',
    'djangotoolbox',
    'social.apps.django_app.default',
    'rest_framework',
    'password_reset',
    'sorl.thumbnail',
)

# Via http://djangotricks.blogspot.com.es/2013/12/how-to-store-your-media-files-in-amazon.html
AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')  # enter your access key id
AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')  # enter your secret access key
if AWS_S3_ACCESS_KEY_ID and AWS_S3_SECRET_ACCESS_KEY:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_S3_SECURE_URLS = False  # use http instead of https
    AWS_QUERYSTRING_AUTH = False  # don't add complex authentication-related query parameters for requests
    AWS_STORAGE_BUCKET_NAME = 'eathub'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    # Anadido para la navegabilidad, de este modo se activa la etiqueta 'active' cuando navegamos.
    'django.core.context_processors.request',
    # Login social
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
      'social.backends.google.GooglePlusAuth',
      'social.backends.facebook.FacebookOAuth2',
      'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_PLUS_KEY = '906981540507-tjpbba4glp7gd91gug9i7glefi04hj8i.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '_ZDnvsQlEviBanm_tb5w35xl'

SOCIAL_AUTH_FACEBOOK_KEY = '1379378712344246'
SOCIAL_AUTH_FACEBOOK_SECRET = '6d393f9ba474e7e81faa1c6fef893c72'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'webapp.views.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

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

from django.core.urlresolvers import reverse
LOGIN_REDIRECT_URL = reverse('main')
LOGIN_URL = reverse('login')

LOCALE_PATHS = (
    os.path.join(BASE_DIR,'locale'),
)

#Configuration for django.core.mail.sendmail
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL', "")
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_PASSWORD', "")
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = 'eat-hub: '
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DJANGO_EMAIL', "")


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DATETIME_FORMAT': ['%s']
}

# Disable SSLify if DEBUG is enabled.
if DEBUG:
    SSLIFY_DISABLE = True