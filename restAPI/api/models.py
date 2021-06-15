from django.db import models
from uuid import uuid4
import json
from .board import Board

# Create your models here.


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    game_json = models.CharField(
        max_length=1000, default=json.dumps(Board().__dict__))
    uuid = models.UUIDField(default=uuid4)
    # players = models.CharField
