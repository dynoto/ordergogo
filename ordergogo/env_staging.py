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
# STARHUB_CELERY_APP_NAME = 'starthub_conexus_dev'
# BROKER_URL = 'redis://localhost:6379/0'
# default RabbitMQ broker
# BROKER_URL = 'amqp://starhub_user:starPasswd@localhost//'

# default RabbitMQ backend
# CELERY_RESULT_BACKEND = 'db+postgresql://starhub_user:starPasswd@localhost/starhub_conexus'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
PAYPAL_MODE = 'sandbox'
PAYPAL_ACCOUNT = 'merchant@ordergogo.co'
PAYPAL_URL = 'api.sandbox.paypal.com'
PAYPAL_CLIENT_ID = 'AcDdgFNuHmYy532RrjCQF3kvvEM8Jaie1bmeGQKqk5wdNPOxKcfLW7BSOZ3v5ZjDVJNcdN07Wax4v-IG'
PAYPAL_SECRET = 'EHtFlVMcsIwCXb2fovR_UGgprcgiSZnb-30QJ0tewxzDXQ1UQkbJP93qgkw36RTf8fowyHlhNVhgqRBM'