from .base import *


DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
