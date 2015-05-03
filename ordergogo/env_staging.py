TEMPLATE_DEBUG = False
DEBUG = False

HOST_URL = 'http://54.169.11.191'
API_SERVER_URL = 'http://stg.getgoru.com'
VERIFY_SSL_CERT = False

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : 'starhub_conexus_user',
        'USER'      : 'starhub_user',
        'PASSWORD'  : 'starPasswd',
        'HOST'      : 'shuser-staging.cjzkaiacwdq1.ap-southeast-1.rds.amazonaws.com',
        'OPTIONS'   : {
            'autocommit' : True,
        }
    },

    'singapore': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : 'starhub_conexus',
        'USER'      : 'starhub_user',
        'PASSWORD'  : 'starPasswd',
        'HOST'      : 'shapi-staging.cjzkaiacwdq1.ap-southeast-1.rds.amazonaws.com',
        'OPTIONS'   : {
            'autocommit' : True,
        }
    }
}

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
    ''
),
'DEFAULT_PERMISSION_CLASSES': (
    'tourist.permissions.TouristToken',
)}

# CELERY SETTINGS
# APP name to distinguish when using the same broker
STARHUB_CELERY_APP_NAME = 'starthub_conexus_staging'
# BROKER_URL = 'redis://localhost:6379/0'
# default RabbitMQ broker
BROKER_URL = 'amqp://starhub_user:starPasswd@userstg.getgoru.com/staging'

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'db+postgresql://starhub_user:starPasswd@shapi-staging.cjzkaiacwdq1.ap-southeast-1.rds.amazonaws.com/starhub_conexus'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'