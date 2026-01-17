import os

from ExcelParser.settings.base import BASE_DIR

SECRET_KEY = 'django-insecure-oi-wmnfizt-srpnggorn94rfzv5o1gu9b51#&9ak%_tohk%azj'
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INITIAL_FILE_NAME_ = 'initial2023'
INITIAL_FILE_PATH_ = os.path.join(BASE_DIR, f'initial_excel_files/{INITIAL_FILE_NAME_}.xlsx')
