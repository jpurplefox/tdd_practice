from rest_framework.response import Response
from rest_framework.views import APIView

from pokemon.models import Pokemon, Move


class Moves(APIView):
    def post(self, request, pk):
        move = Move.objects.get(id=request.data.get('move_id'))
        pokemon = Pokemon.objects.get(pk=pk)
        if move in pokemon.known_moves.all():
            return Response({'error': f'{pokemon.specie} already knows {move.name}'}, status=400)
        if pokemon.known_moves.count() == 4:
            return Response({'error': f'{pokemon.specie} can not learn more than four moves'}, status=400)
        pokemon.known_moves.add(move)
        return Response()
