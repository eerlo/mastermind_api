#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Game(models.Model):
    """
    A game class
    """

    user = models.CharField(max_length=50)
    game_key = models.CharField(max_length=256)
    game_code = models.CharField(max_length=8)
    game_start_datetime = models.DateTimeField(auto_now_add=True)
    solved = models.BooleanField(default=False)


class GameGuess(models.Model):
    """
    Guesses of games
    """
    game = models.ForeignKey(Game, related_name=u'guesses')
    guess = models.CharField(max_length=8)
    exact = models.IntegerField(default=0)
    near = models.IntegerField(default=0)
    guess_datetime = models.DateTimeField(auto_now_add=True)
