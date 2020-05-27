from rest_framework.response import Response
from rest_framework.views import APIView

from pokemon.models import Pokemon, Move


class Moves(APIView):
    def post(self, request, pk):
        move = Move.objects.get(id=request.data.get('move_id'))
        pokemon = Pokemon.objects.get(pk=pk)
        try:
            if pokemon.can_learn(move):
                pokemon.learn(move)
            else:
                return Response({'error': f'{pokemon.specie} can not learn {move.name}'}, 400)
        except pokemon.CanNotLearnMove as e:
            return Response({'error': str(e)}, 400)
        return Response()
