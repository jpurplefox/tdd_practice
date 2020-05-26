import requests


class MoveLearningChecker:
    def a_specie_can_learn(self, specie, move):
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{specie}/')
        moves = [move_data['move']['name'] for move_data in response.json()['moves']]
        return move in moves
