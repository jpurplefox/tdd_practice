from rest_framework.test import APITestCase

from pokemon.models import Trainer, Team, Pokemon, Move


class LearningMovesTestCase(APITestCase):
    def test_a_pokemon_can_learn_a_new_move(self):
        trainer = Trainer.objects.create(name='red', age=16)
        team = Team.objects.create(name='starting team', trainer=trainer)
        charmander = Pokemon.objects.create(specie='charmander', level=5, team=team)

        ember = Move.objects.create(name='ember', power=40)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(charmander.known_moves.count(), 1)
        self.assertIn(ember, charmander.known_moves.all())

    def test_a_pokemon_can_not_learn_a_move_twice(self):
        trainer = Trainer.objects.create(name='red', age=16)
        team = Team.objects.create(name='starting team', trainer=trainer)
        charmander = Pokemon.objects.create(specie='charmander', level=5, team=team)

        ember = Move.objects.create(name='ember', power=40)
        charmander.known_moves.add(ember)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': ember.id})

        self.assertEqual(response.status_code, 400)

        self.assertEqual(charmander.known_moves.count(), 1)
