from django.db import models
from uuid import uuid4
import json
from .board import Board

from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    game_json = models.CharField(
        max_length=1000, default=json.dumps(Board().__dict__))
    uuid = models.UUIDField(default=uuid4)
    full = models.BooleanField(default=False)
    fen = models.CharField(
        max_length=60, default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def __str__(self):
        return "{0}\n{1}\n{2}\n{3}\n{4}\n".format(self.created, self.uuid, self.game_json, str(self.full), self.fen)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    elo = models.IntegerField(default=0)

    class Meta:
        db_table = 'player'


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
    instance.player.save()
