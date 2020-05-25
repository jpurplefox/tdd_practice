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
        self.assertIn('error', response.data)
        self.assertEqual('charmander already knows ember', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 1)

    def test_a_pokemon_can_not_learn_more_than_four_moves(self):
        trainer = Trainer.objects.create(name='red', age=16)
        team = Team.objects.create(name='starting team', trainer=trainer)
        charmander = Pokemon.objects.create(specie='charmander', level=5, team=team)

        scratch = Move.objects.create(name='scratch', power=40)
        growl = Move.objects.create(name='growl', power=0)
        ember = Move.objects.create(name='ember', power=40)
        smokescreen = Move.objects.create(name='smokescreen', power=0)
        charmander.known_moves.add(scratch)
        charmander.known_moves.add(growl)
        charmander.known_moves.add(ember)
        charmander.known_moves.add(smokescreen)

        dragon_breath = Move.objects.create(name='dragon-breath', power=60)

        url = '/pokemon/{}/moves/'.format(charmander.pk)
        response = self.client.post(url, {'move_id': dragon_breath.id})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual('charmander can not learn more than four moves', response.data['error'])

        self.assertEqual(charmander.known_moves.count(), 4)
        self.assertIn(scratch, charmander.known_moves.all())
        self.assertIn(growl, charmander.known_moves.all())
        self.assertIn(ember, charmander.known_moves.all())
        self.assertIn(smokescreen, charmander.known_moves.all())
