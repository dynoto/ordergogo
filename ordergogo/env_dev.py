TEMPLATE_DEBUG = False
DEBUG = False

HOST_URL = 'http://ordergogo.co'
VERIFY_SSL_CERT = False

DATABASES = {
    'default': {
        'ENGINE'    : 'django.contrib.gis.db.backends.postgis',
        'NAME'      : 'ordergogo',
        'USER'      : 'ogg_user',
        'PASSWORD'  : 'password1',
        'HOST'      : '127.0.0.1',
    },
}

# CELERY SETTINGS
# APP name to distinguish when using the same broker
# STARHUB_CELERY_APP_NAME = 'CELERY_HERE'
# BROKER_URL = 'redis://localhost:6379/0'
# default RabbitMQ broker
# BROKER_URL = 'amqp://ordergogo:PASSWORDHERE@localhost//'

# default RabbitMQ backend
# CELERY_RESULT_BACKEND = ''

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
PAYPAL_MODE = 'sandbox'
PAYPAL_ACCOUNT = 'merchant@ordergogo.co'
PAYPAL_URL = 'api.sandbox.paypal.com'
PAYPAL_CLIENT_ID = 'YOUR PAYPAL CLIENT ID'
PAYPAL_SECRET = 'YOUR PAYPAL SECRET ID'