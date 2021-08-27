from api.sockets.json_handler import BoardEncoder
from django.core import serializers
from datetime import datetime
from ..models import Game
# from api.sockets.chesssimul.board import Board
from api.sockets.src.ia.chessBitBoard import Bitboard as Board
import json


def game_handler(sio):
    def join_room(sid, uuid):
        sio.enter_room(sid, str(uuid))
        sio.emit('room_update', {
                 'data': 'another player joined'}, room=str(uuid), skip_sid=sid)

    def left_room(sid, uuid):
        sio.emit('room_update', {
                 'data': 'the other player left'}, room=str(uuid), skip_sid=sid)
        sio.leave_room(sid, str(uuid))

    def close_room(sid, uuid):
        sio.close_room(str(uuid))

    def send_to_room(sid, uuid, msg):
        sio.emit('message', {'data': msg}, room=str(uuid), skip_sid=sid)

    @sio.event
    def get_game(sid, msg):
        """ Retrieve all the games from the database.

        Parameters:
            None

        Response:
            {
                'data': {[game object list]}
            }

        """
        if (msg != None and 'uuid' in msg):
            games = serializers.serialize(
                'json', [Game.objects.get(uuid=msg['uuid'])])
        elif (msg != None and 'uuid' not in msg):
            games = serializers.serialize(
                'json', Game.objects.all(), fields=('created', 'uuid', 'game_json'))
        sio.emit('get_game', {'data': games}, room=sid)

    @sio.event
    def create_game(sid):
        """ Create a new game and persist it in the database.

        Parameters:
            None

        Response:
            {
                'data': {newly created game object}
            }

        """
        game = Game(created=datetime.now())
        board = Board()

        game.game_json = json.dumps(board.__dict__, cls=BoardEncoder)
        game.save()

        print(game.game_json)

        sio.emit('create_game', {'data': serializers.serialize(
            'json', [game], fields=('created', 'uuid'))}, room=sid)
        join_room(sid, game.uuid)

    @sio.event
    def join_game(sid, msg):
        """ Join an existing game if it exists.

        Parameters:
            None

        Response:
            {
                'data': {game object}
            }

        """
        if (msg != None and 'uuid' not in msg):
            games = Game.objects.filter(full=False)
        elif (msg != None and 'uuid' in msg):
            games = Game.objects.filter(uuid=msg['uuid'])
        if (len(games) > 0):
            game = games[0]
            game.full = True
            game.save()
            sio.emit('join_game', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)
        else:
            sio.emit('error', {
                'data': 'No currently joinable game'
            }, room=sid)

    @sio.event
    def new_game(sid):
        """ Enter a game by either creating it if none already exists or by joining an existing one.

        Parameters:
            None

        Response:
            {
                'data': {game object}
            }

        """
        games = Game.objects.filter(full=False)
        if (len(games) > 0):
            game = games[0]
            game.full = True
            game.save()
            sio.emit('join_game', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)
        else:
            game = Game(created=datetime.now())
            board = Board()

            game.game_json = json.dumps(board.__dict__, cls=BoardEncoder)
            game.save()

            sio.emit('create_game', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)

    @ sio.event
    def delete_game(sid, msg):
        """ Delete a game using its unique identifier.

        Parameters:
            {
                'uuid': [game uuid]
            }

        Response:
            None

        """
        uuid = msg['uuid']
        game = Game.objects.get(uuid=uuid)
        game.delete()

    @ sio.event
    def delete_all(sid):
        """ Delete all game objects in database.

        Parameters:
            None

        Response:
            None

        """
        Game.objects.all().delete()
