from django.db import models
from uuid import uuid4
import json
from .board import Board

from django.core.serializers.json import DjangoJSONEncoder

# Create your models here.


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    game_json = models.CharField(
        max_length=1000, default=json.dumps(Board().__dict__))
    uuid = models.UUIDField(default=uuid4)

    def __str__(self):
        return '{"Created" : "{0}", "UUID" : "{1}", "Game" : "{2}"'.format(self.created, self.uuid, self.game_json)
