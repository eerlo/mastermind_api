#-*- coding: utf-8 -*-
import random
import string

VALID_CODE_CHARS = u'RBGYOPCM'

def make_game_key():
    """
    Create a random 256 bits length key
    """
    return ''.join(
                  random.SystemRandom().choice(
                      string.ascii_uppercase + string.digits
                  ) for _ in range(256)
              )


def make_game_code():
    """
    Create a random 8 bits length code
    """
    return ''.join(
                  random.SystemRandom().choice(
                      VALID_CODE_CHARS
                  ) for _ in range(8)
              )

def validate_guess(guess):
    """
    Validate a guess with the game's code.
    """
    correct_code = guess.game.game_code
    exact = 0
    near = 0
    for guess, correct in zip(guess.guess, correct_code):
        if guess == correct:
            exact += 1
        elif guess in correct_code:
            near += 1
    return {u'exact': exact,
            u'near': near}
