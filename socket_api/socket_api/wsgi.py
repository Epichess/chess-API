"""
WSGI config for socket_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import socketio
from api.views import sio
import eventlet
import eventlet.wsgi
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socket_api.settings')

application = get_wsgi_application()


application = socketio.WSGIApp(sio, application)


eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
