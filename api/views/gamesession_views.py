from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout

from ..serializers import UserSerializer, UserRegisterSerializer,  ChangePasswordSerializer, GameSessionSerializer
from ..models.user import User
from ..models.game_session import GameSession, Player

class GameSessions(generics.ListAPIView):
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    serializer_class = GameSessionSerializer
    def get(self, request):
        """Index request"""
        # Get all the games
        gamesessions = GameSession.objects.filter(players__in=[request.user.id])
        # Run the data through the serializer
        print('gamesession(gamesessions)', GameSessionSerializer(gamesessions, many=True))
        data = GameSessionSerializer(gamesessions, many=True).data
        print('gamesessionview data', data)
        return Response({ 'gamesessions': data })