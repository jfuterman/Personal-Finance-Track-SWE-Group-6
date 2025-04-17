"""
WSGI config for wealthwise project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthwise.settings')

application = get_wsgi_application() 