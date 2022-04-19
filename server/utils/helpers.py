import re

def parse_postgres_url(url: str):
    url_regex = 'postgres://(.*?):(.*?)@(.*?):(.*?)/(.*)'
    user, password, host, port, name = re.match(url_regex, url).groups()
    return {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': name,
        'HOST': host,
        'PORT': port,
        'USER': user,
        'PASSWORD': password
    }
