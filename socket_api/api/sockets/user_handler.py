from django.contrib.auth.models import User
from ..models import Player
from django.core import serializers

from django.dispatch import receiver


def user_handler(sio):

    @ sio.event
    def create_user(sid, msg):
        """ Create user and persist it in the database.

        Parameters:
            {
                'username': [username],
                'mail': [e-mail address],
                'password': [password]
            }

        Response:
            {
                'user': {'data': 'User created'}
            }

        """
        try:
            User.objects.create_user(
                msg['username'],
                msg['mail'],
                msg['password']
            )
            sio.emit('user', {'data': 'User created'})
        except Exception as e:
            print(e)
            if (str(e).split(' ')[0] == "UNIQUE"):
                sio.emit(
                    'error', {'data': str(e).split('.')[1] + ' already exists'}, room=sid)

    @sio.event
    def delete_user(sid, msg):
        """ Delete user using his username.

        Parameters:
            {
                'username': [username]
            }

        Response:
            {
                'user': {'data': 'User deleted'}
            }

        """
        try:
            User.objects.get(username=msg['username']).delete()
            sio.emit('user', {'data': 'User deleted'})
        except Exception as e:
            if (str(e) == "User matching query does not exist."):
                sio.emit(
                    'error', {'data': 'User doesn\'t exists'}
                )
            pass

    @sio.event
    def get_user(sid, msg):
        """ Retrieve user using his username.

        Parameters:
            {
                'username': [username]
            }

        Response:
            {
                'user': {player object}
            }

        """
        try:
            user = User.objects.get(username=msg['username'])
            sio.emit('user', {'data': serializers.serialize(
                'json', [user, user.player])})
        except Exception as e:
            print(e)
            sio.emit(
                'error', {'data': 'User doesn\'t exists'}
            )
            pass

    @sio.event
    def get_users(sid):
        """ Retrieve all the users in database.

        Parameters:
            None

        Response:
            {
                'user': [{player object}]
            }

        """
        try:
            users = User.objects.all()
            sio.emit('user', {'data': serializers.serialize('json', users)})
        except Exception as e:
            print(e)
            pass
