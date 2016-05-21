#-*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import list_route
from rest_framework.response import Response


from core.models import Game
from core.serializers import CreateGameSerializer, NewGuessSerializer
from core import utils

class CreateNewGameView(viewsets.GenericViewSet):
    """
    New game endpoint.
    """
    serializer_class=CreateGameSerializer

    @list_route(methods=[u'POST'],
                url_path=u'create-new-game',
                serializer_class=CreateGameSerializer)
    def create_new_game(self, request):
        """
        Creates a new game, just give-me your name :)
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()
        return Response({u'game_key': instance.game_key},
                        status=status.HTTP_201_CREATED)

class MakeNewGuessView(viewsets.GenericViewSet):
    """
    Guesses endpoint.
    """
    serializer_class = NewGuessSerializer

    @list_route(methods=[u'POST'],
                url_path=u'make-new-guess',
                serializer_class=NewGuessSerializer)
    def make_new_guess(self, request):
        """
        Make a new guess! Give-me the game key and your guess!
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()
        game = instance.game
        guess_result = utils.validate_guess(instance)

        if guess_result[u'exact'] == 8:
            game.solved = True
            game.save()
        instance.exact = guess_result[u'exact']
        instance.near = guess_result[u'near']
        return Response({u'game_key': game.game_key,
                         u'colors': list(utils.VALID_CODE_CHARS),
                         u'solved': game.solved,
                         u'num_guesses': game.guesses.count(),
                         u'result': {
                             u'exact': instance.exact,
                             u'near': instance.near
                         }},
                        status=status.HTTP_201_CREATED)
