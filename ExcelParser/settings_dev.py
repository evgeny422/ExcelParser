from ExcelParser.settings import BASE_DIR

SECRET_KEY = 'django-insecure-oi-wmnfizt-srpnggorn94rfzv5o1gu9b51#&9ak%_tohk%azj'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
