TEMPLATE_DEBUG = False
DEBUG = False

HOST_URL = 'http://54.169.11.191'
API_SERVER_URL = 'https://www.getgoru.com'
VERIFY_SSL_CERT = True

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : 'starhub_conexus_user',
        'USER'      : 'starhub_user',
        'PASSWORD'  : 'starPasswd',
        'HOST'      : 'starhubconexususer.cjzkaiacwdq1.ap-southeast-1.rds.amazonaws.com',
        'OPTIONS'   : {
            'autocommit' : True,
        }
    },

    'singapore': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : 'starhub_conexus',
        'USER'      : 'starhub_user',
        'PASSWORD'  : 'starPasswd',
        'HOST'      : 'starhubconexus.cjzkaiacwdq1.ap-southeast-1.rds.amazonaws.com',
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

# Add secure flag for session on live server
SESSION_COOKIE_SECURE = True

# CELERY SETTINGS
# APP name to distinguish when using the same broker
STARHUB_CELERY_APP_NAME = 'starthub_conexus_prelive'
# BROKER_URL = 'redis://localhost:6379/0'
# default RabbitMQ broker
BROKER_URL = 'amqp://starhub_user:starPasswd@userstg.getgoru.com/live'

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'db+postgresql://starhub_user:starPasswd@starhubconexus.cjzkaiacwdq1.ap-southeast-1.rds.amazonaws.com/starhub_conexus'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'