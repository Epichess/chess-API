# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
import socketio
from django.http import HttpResponse
import os
from django.core import serializers
from datetime import datetime
import json
from api.models import Game
from api.sockets.game_handler import game_handler
from api.sockets.user_handler import user_handler
from api.sockets.move_handler import move_handler
async_mode = None


basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode, cors_allowed_origins='*')
thread = None


def index(request):
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


# socket-io game relative event
game_handler(sio)
# socket-io user relative event
user_handler(sio)
# socket-io move relative event
move_handler(sio)


@sio.event
def pong(sid, message):
    sio.emit('pong', {'data': message['text']})


@sio.event
def chat(sid, message):
    data = json.loads(message)
    sio.emit('response', {'data': data['text']},
             room=data['uuid'], skip_sid=sid)


@ sio.event
def connect(sid, environ):
    sio.emit('response', {'data': 'Connected', 'count': 0}, room=sid)


@ sio.event
def disconnect(sid):
    print('Client disconnected')


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)
