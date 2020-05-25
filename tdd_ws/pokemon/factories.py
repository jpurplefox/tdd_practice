import factory

from pokemon.models import Pokemon, Team, Trainer, Move


class TrainerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Trainer

    name = factory.Sequence(lambda n: 'Trainer {}'.format(n + 1))
    age = 16


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: 'Team {}'.format(n + 1))
    trainer = factory.SubFactory(TrainerFactory)


class PokemonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Pokemon

    level = 5
    team = factory.SubFactory(TeamFactory)


class MoveFactory(factory.DjangoModelFactory):
    class Meta:
        model = Move

    name = factory.Sequence(lambda n: 'Move {}'.format(n + 1))
    power = 40
