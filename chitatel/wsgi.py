"""
=============
chitatel.wsgi
=============

Our WSGI application to use with Gunicorn or uWSGI.

"""

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chitatel.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
