TEMPLATE_DEBUG = True
DEBUG = True

HOST_URL = 'http://ordergogo.local'
VERIFY_SSL_CERT = False

DATABASES = {
    'default': {
        'ENGINE'    : 'django.contrib.gis.db.backends.postgis',
        'NAME'      : 'ordergogo',
        'USER'      : 'ogg_user',
        'PASSWORD'  : 'password1',
        'HOST'      : '127.0.0.1',
        'OPTIONS'   : {
            'autocommit' : True,
        }
    },
}

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
    ''
),
'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.AllowAny',
)}

# CELERY SETTINGS
# APP name to distinguish when using the same broker
# STARHUB_CELERY_APP_NAME = 'starthub_conexus_dev'
# BROKER_URL = 'redis://localhost:6379/0'
# default RabbitMQ broker
# BROKER_URL = 'amqp://starhub_user:starPasswd@localhost//'

# default RabbitMQ backend
# CELERY_RESULT_BACKEND = 'db+postgresql://starhub_user:starPasswd@localhost/starhub_conexus'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'