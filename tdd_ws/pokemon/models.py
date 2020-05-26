from django.db import models

from pokemon.integrations import MoveLearningChecker

move_learning_checker = MoveLearningChecker()


class Move(models.Model):
    name = models.CharField(max_length=200)
    power = models.IntegerField()


class Trainer(models.Model):
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=200)


class Team(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Pokemon(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    specie = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    level = models.IntegerField()
    known_moves = models.ManyToManyField(Move)

    class CanNotLearnMove(Exception):
        pass

    def learn(self, move):
        if self.known_moves.count() == 4:
            raise self.CanNotLearnMove(f'{self.specie} can not learn more than four moves')
        if move in self.known_moves.all():
            raise self.CanNotLearnMove(f'{self.specie} already knows {move.name}')
        self.known_moves.add(move)

    def can_learn(self, move):
        return move_learning_checker.a_specie_can_learn(self.specie, move.name)
