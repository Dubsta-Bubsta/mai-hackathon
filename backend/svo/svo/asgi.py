import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from airline.consumers import AirlineConsumer
from dispatcher.consumers import DispatcherConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'svo.settings')
django.setup()

application = ProtocolTypeRouter(dict(http=URLRouter([
    re_path(r"", AsgiHandler()),
]), websocket=URLRouter([
    path("ws/airline/<int:airline_id>/", AirlineConsumer.as_asgi()),
    path("ws/dispatcher/", DispatcherConsumer.as_asgi())
])))
