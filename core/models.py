#-*- coding: utf-8 -*-
"""
Application core models
"""
from __future__ import unicode_literals

from django.db import models

class Game(models.Model):
    """
    A game class
    """

    user = models.CharField(
               verbose_name=u'Game User',
               max_length=50
           )
    game_key = models.CharField(
                   verbose_name=u'Game key',
                   max_length=256,
                   unique=True
               )
    game_code = models.CharField(
                    verbose_name=u'Game Code',
                    max_length=8
                )
    game_start_datetime = models.DateTimeField(
                              verbose_name=u'Game start datetime(auto)',
                              auto_now_add=True
                          )
    solved = models.BooleanField(
                 verbose_name=u'Game Already Solved',
                 default=False
             )


class GameGuess(models.Model):
    """
    Guesses of games
    """
    game = models.ForeignKey(
               verbose_name=u'Game',
               to=Game,
               related_name=u'guesses'
           )
    guess = models.CharField(
                verbose_name=u'Guess',
                max_length=8
            )
    exact = models.IntegerField(
                verbose_name=u'Number of Exact Colors',
                default=0
            )
    near = models.IntegerField(
               verbose_name=u'Number of Near Colors',
               default=0
           )
    guess_datetime = models.DateTimeField(
                         verbose_name=u'Guess datetime(auto)',
                         auto_now_add=True
                     )
