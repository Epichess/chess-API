from rest_framework import viewsets, response
from .serializers import GameSerializer
from .models import Game
from uuid import uuid4

import json


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'uuid'

    def create(self, request):
        '''
        (POST) /games
        Creates a new Game, stores it in database and returns its ID
        Returns newly created game ID (String)
        '''
        print(request.data)
        new_uuid = uuid4()
        new_game = {"uuid": new_uuid}
        request.data.update(new_game)
        super().create(request)
        return response.Response(data=str(new_uuid))

    def list(self, request):
        '''
        (GET) /games
        Retrieve a list of games from the database
        Returns a JSON object containing the games
        foo = json.dumps(Square().__dict__)
        '''
        return super().list(request)
