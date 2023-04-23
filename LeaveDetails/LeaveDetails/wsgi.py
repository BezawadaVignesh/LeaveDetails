"""
WSGI config for LeaveDetails project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LeaveDetails.settings')

application = get_wsgi_application()


# assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/MyWebApp70/LeaveDetails'
if path not in sys.path:
    sys.path.insert(0, path)