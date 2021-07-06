from django.core import serializers
from datetime import datetime
from ..models import Game


def game_handler(sio):
    def join_room(sid, uuid):
        sio.enter_room(sid, uuid)

    def left_room(sid, uuid):
        sio.leave_room(sid, uuid)

    def close_room(sid, uuid):
        sio.close_room(uuid)

    def send_to_room(uuid, msg):
        sio.emit('message', {'data': msg}, room=uuid)

    @sio.event
    def get_games(sid):
        games = serializers.serialize(
            'json', Game.objects.all(), fields=('created', 'uuid', 'game_json'))
        sio.emit('games', {'data': games}, room=sid)

    @sio.event
    def get_by_uuid(sid, message):
        games = serializers.serialize(
            'json', [Game.objects.get(uuid=message['uuid'])])
        sio.emit('response', {'data': games}, room=sid)

    @sio.event
    def create_game(sid):
        new_game = Game(created=datetime.now())
        new_game.save()
        sio.emit('creating', {'data': serializers.serialize(
            'json', [new_game], fields=('created', 'uuid'))}, room=sid)
        join_room(sid, new_game.uuid)

    @sio.event
    def join_game(sid):
        games = Game.objects.filter(full=False)
        # check opponent level ?
        if (len(games) > 0):
            game = games[0]
            game.full = True
            game.save()
            sio.emit('joining', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)
        else:
            sio.emit('error', {
                'data': 'No currently joinable game'
            }, room=sid)

    @sio.event
    def join_game_uuid(sid, msg):
        games = Game.objects.filter(uuid=msg['uuid'])
        if (len(games) > 0):
            game = games[0]
            game.full = True
            game.save()
            sio.emit('joining', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)
        else:
            sio.emit('error', {
                'data': 'No currently joinable game'
            }, room=sid)

    @sio.event
    def new_game(sid):
        games = Game.objects.filter(full=False)
        # check opponent level ?
        if (len(games) > 0):
            game = games[0]
            game.full = True
            game.save()
            sio.emit('joining', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)
        else:
            game = Game(created=datetime.now())
            game.save()
            sio.emit('creating', {'data': serializers.serialize(
                'json', [game], fields=('created', 'uuid'))}, room=sid)
            join_room(sid, game.uuid)

    @sio.event
    def delete_game(sid, msg):
        uuid = msg['uuid']
        game = Game.objects.get(uuid=uuid)
        game.delete()

    @sio.event
    def delete_all(sid):
        Game.objects.all().delete()
