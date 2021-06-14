from django.db import models
from uuid import uuid4

# Create your models here.


class Game(models.Model):
    fen_line = models.CharField(
        max_length=100, default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    uuid = models.UUIDField(default=uuid4)
