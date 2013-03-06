import os, sys
WSGIPythonHome /home/django/django-get2

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

os.environ['DJANGO_SETTINGS_MODULE'] = 'get2.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

