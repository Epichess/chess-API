from .consumers import GameConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

websockets = URLRouter([
    path(
        "ws/game/<str:uuid>", GameConsumer.as_asgi(),
        name="game",
    ),
])
