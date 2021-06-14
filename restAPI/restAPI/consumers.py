import json
from threading import Event
import channels

from channels.exceptions import DenyConnection, StopConsumer
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser


class GameConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("[info] new client connected")
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    def websocket_disconnect(self, event):
        print("[info] client disconnected")
        raise StopConsumer
