"""
WSGI config for instagram_config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_config.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root='/Users/jordan/kenzieProjects/SEQ4/capstone_insta/static')
application.add_files('/Users/jordan/kenzieProjects/SEQ4/capstone_insta/media')
