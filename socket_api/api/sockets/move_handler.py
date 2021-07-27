from django.core import serializers
from datetime import datetime
from api.sockets.json_handler import BoardDecoder, BoardEncoder
from ..models import Game
# from api.sockets.chesssimul.board import Board
# from api.sockets.chesssimul.move import Move
import json


def move_handler(sio):

    def translate_coord(start, end):
        start_coord = [7 - (ord(start[1]) - 49),
                       (ord(start[0].upper()) - 65)]
        end_coord = [7 - (ord(end[1]) - 49),
                     (ord(end[0].upper()) - 65)]
        return (start_coord, end_coord)

    @sio.event
    def make_move(sid, message):
        uuid = message['uuid']
        start = message['start']
        end = message['end']
        game = Game.objects.get(uuid=uuid)

        board = BoardDecoder(json.loads(game.game_json))

        coord = translate_coord(start, end)
        move = Move(coord[0], coord[1])

        if (board.make_move(move)):
            game.game_json = json.dumps(board.__dict__, cls=BoardEncoder)
            game.save()
            sio.emit('move', {'data': 'success', 'legal': 'true'})
        else:
            sio.emit('move', {'data': 'move isn\'t legal', 'legal': 'false'})
