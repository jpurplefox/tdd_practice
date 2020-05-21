from django.db import models


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
