from unittest.mock import patch

from rest_framework.test import APITestCase

from pokemon.factories import PokemonFactory, MoveFactory


class FakeResponse:
    def __init__(self, data, status_code, ok):
        self.data = data
        self.status_code = status_code
        self.ok = ok

    def json(self):
        return self.data


class FakeRequests:
    def __init__(self, get_responses):
        self.get_responses = get_responses

    def get(self, path):
        try:
            data = self.get_responses[path]
            response = FakeResponse(data, 200, True)
        except KeyError:
            response = FakeResponse({}, 404, False)

        return response


class LearningMovesTestCase(APITestCase):
    def test_a_pokemon_can_learn_a_new_move(self):
        fake_requests = FakeRequests({
            'https://pokeapi.co/api/v2/pokemon/charmander/': {
                'moves': [
                    {'move': {'name': 'ember', 'url': 'https://pokeapi.co/api/v2/move/52/'}},
                ]
            }
        })
        charmander = PokemonFactory(specie='charmander')

        ember = MoveFactory(name='ember', power=40)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        with patch('pokemon.models.requests', fake_requests):
            response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(charmander.known_moves.count(), 1)
        self.assertIn(ember, charmander.known_moves.all())

    def test_a_pokemon_can_not_learn_a_move_twice(self):
        fake_requests = FakeRequests({
            'https://pokeapi.co/api/v2/pokemon/charmander/': {
                'moves': [
                    {'move': {'name': 'ember', 'url': 'https://pokeapi.co/api/v2/move/52/'}},
                ]
            }
        })
        charmander = PokemonFactory(specie='charmander')

        ember = MoveFactory(name='ember', power=40)
        charmander.learn(ember)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        with patch('pokemon.models.requests', fake_requests):
            response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander already knows ember', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 1)

    def test_a_pokemon_can_not_learn_more_than_four_moves(self):
        fake_requests = FakeRequests({
            'https://pokeapi.co/api/v2/pokemon/charmander/': {
                'moves': [
                    {'move': {'name': 'dragon-breath', 'url': 'https://pokeapi.co/api/v2/move/225/'}},
                ]
            }
        })
        charmander = PokemonFactory(specie='charmander')
        for move in MoveFactory.create_batch(4):
            charmander.learn(move)

        dragon_breath = MoveFactory(name='dragon-breath', power=60)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        with patch('pokemon.models.requests', fake_requests):
            response = self.client.post(url, {'move_id': dragon_breath.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander can not learn more than four moves', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 4)
        self.assertNotIn(dragon_breath, charmander.known_moves.all())

    def test_a_pokemon_can_not_learn_a_move_not_available_for_his_specie(self):
        fake_requests = FakeRequests({
            'https://pokeapi.co/api/v2/pokemon/charmander/': {
                'moves': [
                    {'move': {'name': 'ember', 'url': 'https://pokeapi.co/api/v2/move/52/'}},
                ]
            }
        })
        charmander = PokemonFactory(specie='charmander')

        bubble = MoveFactory(name='bubble', power=40)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        with patch('pokemon.models.requests', fake_requests):
            response = self.client.post(url, {'move_id': bubble.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander can not learn bubble', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 0)
