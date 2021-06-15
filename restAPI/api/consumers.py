import json
from threading import Event
import channels

from channels.exceptions import DenyConnection, StopConsumer
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from asgiref.sync import async_to_sync

from channels.db import database_sync_to_async


from api.models import Game
from api.serializers import GameSerializer

from asgiref.sync import async_to_sync


class GameConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("[info] new client connected")
        # Game.objects.filter(
        #     uuid=self.scope['url_route']['kwargs']['uuid']).update(id=1)
        # print(self.channel_name)
        self.send({
            "type": "websocket.accept",
        })

    def get_game(self):
        return Game.objects.filter(
            uuid=self.scope['url_route']['kwargs']['uuid'])

    def websocket_receive(self, event):
        game = self.get_game()
        data = json.loads(event['text'])
        self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    def websocket_disconnect(self, event):
        print("[info] client disconnected")
        raise StopConsumer
