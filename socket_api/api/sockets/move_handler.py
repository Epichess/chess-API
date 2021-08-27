from django.core import serializers
from datetime import datetime
from api.sockets.json_handler import BoardDecoder, BoardEncoder
from ..models import Game
from api.sockets.src.ia.move import Move
import json


def move_handler(sio):

    def translate_coord(start, end):
        start_index = (ord(start[0].upper()) - 65) + ((int(start[1]) - 1) * 8)
        end_index = (ord(end[0].upper()) - 65) + ((int(end[1]) - 1) * 8)

        return (start_index, end_index)

    @sio.event
    def make_move(sid, message):
        """ Check a move legality and tries to make it.

        Parameters:
            {
                'uuid': [game uuid],
                'start': [starting square e.g. 'A2'],
                'end': [ending square e.g. 'A2']
            }

        Response:
            {
                'data': [message],
                'legal': [boolean]
            }

        """
        uuid = message['uuid']
        start = message['start']
        end = message['end']
        game = Game.objects.get(uuid=uuid)

        print("START")
        print(start)
        print("END")
        print(end)

        sio.emit('make_move', {'data': {'fen': 'le move est pas processed'}})
        return

        board = BoardDecoder(json.loads(game.game_json))

        coord = translate_coord(start, end)
        move = Move(coord[0], coord[1], 1, 0)

        if (board.make_move(move)):
            game.game_json = json.dumps(board.__dict__, cls=BoardEncoder)
            game.save()
            sio.emit('move', {'data': 'success', 'legal': 'true'})
        else:
            sio.emit('move', {'data': 'move isn\'t legal', 'legal': 'false'})

    @sio.event
    def ask_move(sid, message):
        """ Returns possible move starting from a given square.

        Parameters:
            {
                'uuid': [game uuid],
                'start': [starting square e.g. 'A2'],
                'end': [ending square e.g. 'A2']
            }

        Response:
            {
                'data': [message],
                'legal': [boolean]
            }

        """
        sio.emit('ask_move', {'data': 'EN COURS DE DEPLOIEMENT'})
