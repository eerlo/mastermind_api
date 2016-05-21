#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from rest_framework import serializers

from core.models import Game, GameGuess
from core.utils import make_game_key, make_game_code, VALID_CODE_CHARS

class CreateGameSerializer(serializers.ModelSerializer):
    """
    Serializer to create a new game.
    """

    class Meta:
        model = Game
        fields = [u'user',]

    def create(self, validated_data):
        """
        Start a new game.
        """
        created = Game.objects.create(
                      game_key=make_game_key(),
                      game_code=make_game_code(),
                      user=validated_data[u'user']
                  )
        return created


class NewGuessSerializer(serializers.ModelSerializer):
    """
    Serializer to a new guess.
    """
    game_key = serializers.CharField(max_length=256)

    class Meta:
        model = GameGuess
        fields = [u'game_key', 'guess',]

    def validate_guess(self, value):
        """
        Validate the guess length and content.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                    u'Guess must be a 8 bit string.'
                  )

        if [1 for i in value if i not in VALID_CODE_CHARS]:
            raise serializers.ValidationError(
                    u'Invalid chars in guess, must be "%s".' % VALID_CODE_CHARS
                  )
        return value

    def validate_game_key(self, value):
        try:
            game = Game.objects.get(game_key=value)
        except Game.DoesNotExist:
            raise serializers.ValidationError(u'Invalid game key.')

        if game.game_start_datetime > datetime.now() + timedelta(minutes=5):
            raise serializers.ValidationError(u'Game key expired.')

        if game.solved:
            raise serializers.ValidationError(u'Game already solved.')

        return value



    def create(self, validated_data):
        """
        Start a new game.
        """
        game = Game.objects.get(game_key=validated_data[u'game_key'])
        created = GameGuess.objects.create(
                      game=game,
                      guess=validated_data[u'guess']
                  )
        return created        

