#-*- coding: utf-8 -*-
import json
from datetime import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse

"""
Application core unit test cases
"""
from core import models, utils, serializers

class CoreUtilsTestCase(TestCase):
    """
    utils.py module test cases.
    """
    fixtures = (u'core/fixtures/game1.json',)

    def test_make_game_key(self):
        """
        Tests a new game key creation
        """
        game_key1 = utils.make_game_key()
        game_key2 = utils.make_game_key()

        self.assertEqual(len(game_key1), len(game_key2))
        self.assertEqual(len(game_key1), 256)
        self.assertNotEqual(game_key1, game_key2)


    def test_make_game_code(self):
        """
        Tests a new game secret code creation
        """
        game_code1 = utils.make_game_code()
        game_code2 = utils.make_game_code()

        self.assertEqual(len(game_code1), len(game_code2))
        self.assertEqual(len(game_code1), 8)

        for i in game_code1:
            self.assertTrue(i in utils.VALID_CODE_CHARS)

        for i in game_code2:
            self.assertTrue(i in utils.VALID_CODE_CHARS)

    def test_validate_guess(self):
        """
        Test the validation of guesses
        """
        game = models.Game.objects.get(pk=1)
        not_solved = game.guesses.get(exact=2, near=6)
        solved = game.guesses.get(exact=8)

        result1 = utils.validate_guess(not_solved)
        self.assertEqual(result1[u'exact'], 2)
        self.assertEqual(result1[u'near'], 6)

        result2 = utils.validate_guess(solved)
        self.assertEqual(result2[u'exact'], 8)
        self.assertEqual(result2[u'near'], 0)



class CreateGameSerializerTestCase(TestCase):
    """
    Test regarding the serializer used to create a new game.
    """

    def test_is_valid(self):
        """
        Test when it may be valid
        """
        serializer = serializers.CreateGameSerializer(
                         data={u'user': u'Eduardo Erlo'}
                     )
        self.assertTrue(serializer.is_valid())


    def test_is_invalid(self):
        """
        Test when it may not be valid
        """
        serializer = serializers.CreateGameSerializer(
                         data={}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'user'))

    def test_create(self):
        """
        Test the serializer's create method
        """
        game_count_before = models.Game.objects.all().count()
        serializer = serializers.CreateGameSerializer(
                         data={u'user': u'Eduardo Erlo'}
                     )
        self.assertTrue(serializer.is_valid())
        created = serializer.create(serializer.validated_data)

        game_count_after = models.Game.objects.all().count()

        self.assertEqual(game_count_before+1, game_count_after)


class NewGuessSerializerTestCase(TestCase):
    """
    Test regarding the serializer used to create a new guess.
    """
    fixtures = (u'core/fixtures/game1.json',)


    def setUp(self):
        """
        Set ups to make the test methods ready to execute
        """
        self.game_instance = models.Game.objects.get(pk=1)

        #set the game start datetime to a valid time(not 5 minutes expired)
        self.game_instance.game_start_datetime = datetime.now()
        self.game_instance.save()


    def test_is_valid(self):
        """
        Test when it may be valid
        """
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBYPPBGB'}
                     )
        self.assertTrue(serializer.is_valid())


    def test_is_invalid(self):
        """
        Test when it may not be valid
        """
        serializer = serializers.NewGuessSerializer(
                         data={}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'game_key'))
        self.assertTrue(serializer.errors.has_key(u'guess'))


    def test_invalid_guesses(self):
        """
        Test invalid guesses serializer validation
        """
        #Test with an no 8 bit guess(lower)
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBGB'}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'guess'))

        #Test with an no 8 bit guess(higher)
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBGBBBBBB'}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'guess'))

        #Test with invalid colors
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBGBXBBB'}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'guess'))


    def test_invalid_game_keys(self):
        """
        Test invalid game keys serializer validation
        """
        #Test with an inexistent game key
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': u'invalid key',
                               u'guess': u'PBGBBBPY'}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'game_key'))

        #Test with a valid but 5-minutes expired game key
        self.game_instance.game_start_datetime = datetime(2010, 1, 1)
        self.game_instance.save()
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBGBBBBB'}
                     )

        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'game_key'))

        #Test with a valid and time-ok game key, but for a already solved game
        self.game_instance.game_start_datetime = datetime.now()
        self.game_instance.solved = True
        self.game_instance.save()
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBGBXBBB'}
                     )
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors.has_key(u'game_key'))


    
    def test_create(self):
        """
        Test the serializer's create method
        """
        guess_count_before = self.game_instance.guesses.all().count()
        serializer = serializers.NewGuessSerializer(
                         data={u'game_key': self.game_instance.game_key,
                               u'guess': u'PBGBYBBB'}
                     )

        self.assertTrue(serializer.is_valid())
        created = serializer.create(serializer.validated_data)

        guess_count_after = self.game_instance.guesses.all().count()

        self.assertEqual(guess_count_before+1, guess_count_after)


class CreateNewGameViewTestCase(TestCase):
    """
    Test the new game create endpoint
    """

    def test_invalid_request(self):
        """
        Test invalid requests handling
        """
        url = reverse(u'games-create-new-game')

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(url, data={})
        self.assertEqual(post_response.status_code, 400)


    def test_valid_request(self):
        """
        Test valid requests handling
        """
        url = reverse(u'games-create-new-game')

        post_response = self.client.post(url, data={u'user': u'Eduardo Erlo'})
        self.assertEqual(post_response.status_code, 201)
        parsed_content = json.loads(post_response.content)
        self.assertTrue(parsed_content.has_key(u'game_key'))
        self.assertEqual(
            parsed_content[u'game_key'],
            models.Game.objects.latest(u'pk').game_key
        )


class MakeNewGuessViewTestCase(TestCase):
    """
    Test the new guess meking endpoint
    """
    fixtures = (u'core/fixtures/game1.json',)


    def setUp(self):
        """
        Set ups to make the test methods ready to execute
        """
        self.game_instance = models.Game.objects.get(pk=1)

        #set the game start datetime to a valid time(not 5 minutes expired)
        self.game_instance.game_start_datetime = datetime.now()
        self.game_instance.save()


    def test_invalid_request(self):
        """
        Test invalid requests handling
        """
        url = reverse(u'guesses-make-new-guess')

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(url, data={})
        self.assertEqual(post_response.status_code, 400)


    def test_valid_request(self):
        """
        Test valid requests handling
        """
        url = reverse(u'guesses-make-new-guess')

        post_response = self.client.post(
                            url,
                            data={u'game_key': self.game_instance.game_key,
                                  u'guess': u'YBPYGPGP'}
                        )

        self.assertEqual(post_response.status_code, 201)
        parsed_content = json.loads(post_response.content)
        self.assertTrue(parsed_content.has_key(u'game_key'))
        self.assertTrue(parsed_content.has_key(u'result'))
        self.assertTrue(parsed_content.has_key(u'solved'))
        self.assertTrue(parsed_content.has_key(u'colors'))
        self.assertTrue(parsed_content.has_key(u'num_guesses'))

        self.assertEqual(parsed_content[u'result'], {"near":5,"exact":2})
        self.assertEqual(
            parsed_content[u'game_key'],
            self.game_instance.game_key
        )
        self.assertEqual(parsed_content[u'solved'], False)
        self.assertEqual(parsed_content[u'num_guesses'], 3)


        #now, a post response with the correct code, to check the "solved=True"
        post_response = self.client.post(
                            url,
                            data={u'game_key': self.game_instance.game_key,
                                  u'guess': self.game_instance.game_code}
                        )
        parsed_content = json.loads(post_response.content)
        self.assertEqual(parsed_content[u'solved'], True)
