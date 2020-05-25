from rest_framework.response import Response
from rest_framework.views import APIView

from pokemon.models import Pokemon, Move


class Moves(APIView):
    def post(self, request, pk):
        move = Move.objects.get(id=request.data.get('move_id'))
        pokemon = Pokemon.objects.get(pk=pk)
        if move in pokemon.known_moves.all():
            return Response({}, status=400)
        pokemon.known_moves.add(move)
        return Response()
