from unittest.mock import patch

from rest_framework.test import APITestCase

from pokemon.factories import PokemonFactory, MoveFactory


class LearningMovesTestCase(APITestCase):
    @patch('pokemon.models.requests')
    def test_a_pokemon_can_learn_a_new_move(self, requests_mock):
        requests_mock.get.return_value.ok = True
        requests_mock.get.return_value.json.return_value = {
            'moves': [
                {'move': {'name': 'ember', 'url': 'https://pokeapi.co/api/v2/move/52/'}},
            ]
        }
        charmander = PokemonFactory(specie='charmander')

        ember = MoveFactory(name='ember', power=40)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(charmander.known_moves.count(), 1)
        self.assertIn(ember, charmander.known_moves.all())

    @patch('pokemon.models.requests')
    def test_a_pokemon_can_not_learn_a_move_twice(self, requests_mock):
        requests_mock.get.return_value.ok = True
        requests_mock.get.return_value.json.return_value = {
            'moves': [
                {'move': {'name': 'ember', 'url': 'https://pokeapi.co/api/v2/move/52/'}},
            ]
        }
        charmander = PokemonFactory(specie='charmander')

        ember = MoveFactory(name='ember', power=40)
        charmander.learn(ember)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander already knows ember', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 1)

    @patch('pokemon.models.requests')
    def test_a_pokemon_can_not_learn_more_than_four_moves(self, requests_mock):
        requests_mock.get.return_value.ok = True
        requests_mock.get.return_value.json.return_value = {
            'moves': [
                {'move': {'name': 'dragon-breath', 'url': 'https://pokeapi.co/api/v2/move/225/'}},
            ]
        }
        charmander = PokemonFactory(specie='charmander')
        for move in MoveFactory.create_batch(4):
            charmander.learn(move)

        dragon_breath = MoveFactory(name='dragon-breath', power=60)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': dragon_breath.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander can not learn more than four moves', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 4)
        self.assertNotIn(dragon_breath, charmander.known_moves.all())

    @patch('pokemon.models.requests')
    def test_a_pokemon_can_not_learn_a_move_not_available_for_his_specie(self, requests_mock):
        requests_mock.get.return_value.ok = True
        requests_mock.get.return_value.json.return_value = {
            'moves': [
                {'move': {'name': 'ember', 'url': 'https://pokeapi.co/api/v2/move/52/'}},
            ]
        }
        charmander = PokemonFactory(specie='charmander')

        bubble = MoveFactory(name='bubble', power=40)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': bubble.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander can not learn bubble', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 0)
