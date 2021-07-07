from django.core import serializers
from datetime import datetime
from ..models import Game
from api.sockets.chesssimul.board import Board
from api.sockets.chesssimul.coup import Move


def move_handler(sio):

    @sio.event
    def make_move(sid, message):
        uuid = message['uuid']
        start = message['start']
        end = message['end']
        game = Game.objects.get(uuid=uuid)

        board = Board()
        move = Move((), ())
        board.make_move()
        # result = send_to_back (game, move)
        # if (result == valide)
        # sio.emit('move', {'data': 'game'}, room=uuid)
        # else
        # sio.emit('error', {'data': 'illegal'}, room=sid)
