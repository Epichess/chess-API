from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from django.core import serializers
from datetime import datetime
from api.sockets.json_handler import BoardDecoder, BoardEncoder
from ..models import Game
from api.sockets.src.ia.move import Move
from api.sockets.src.ia.gameApi import GameChecker
import json


def move_handler(sio):

    def translate_coord(start, end):
        start_index = (7 - start['row']) * 8 + (start['col'])
        end_index = (7 - end['row']) * 8 + (end['col'])

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
        coord = translate_coord(start, end)

        print(start, end)
        print(coord)
        print(game)

        gc = GameChecker(game.fen)
        move = gc.makeMoveAPI(coord[0], coord[1])

        game.fen = move.fen
        game.save()

        sio.emit('make_move', {
            'isMoveValid': move.isMoveValid,
            'isKingCheck': move.isKingCheck,
            'isGameOver': move.isGameOver,
            'fen': move.fen,
            'start': start,
            'end': end
        }, room=uuid)

        # sio.emit('make_move', {'data': 'fen'},
        #      room=uuid)

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
