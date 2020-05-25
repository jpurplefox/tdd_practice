from rest_framework.test import APITestCase

from pokemon.factories import PokemonFactory, MoveFactory


class LearningMovesTestCase(APITestCase):
    def test_a_pokemon_can_learn_a_new_move(self):
        charmander = PokemonFactory(specie='charmander')

        ember = MoveFactory(name='ember', power=40)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(charmander.known_moves.count(), 1)
        self.assertIn(ember, charmander.known_moves.all())

    def test_a_pokemon_can_not_learn_a_move_twice(self):
        charmander = PokemonFactory(specie='charmander')

        ember = MoveFactory(name='ember', power=40)
        charmander.learn(ember)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander already knows ember', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 1)

    def test_a_pokemon_can_not_learn_more_than_four_moves(self):
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
