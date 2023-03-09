from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication
from rest_framework import status, generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import random

from ..serializers import UserSerializer, UserRegisterSerializer,  ChangePasswordSerializer, GameSessionSerializer
from ..models.user import User
from ..models.game_session import GameSession, Player, Question

class GameSessions(generics.ListAPIView):
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    serializer_class = GameSessionSerializer
    def get(self, request):
        """Index request"""
        # Get all the games
        gamesessions = GameSession.objects.filter(players__in=[request.user.id])
        # Run the data through the serializer
        # print('gamesession(gamesessions)', GameSessionSerializer(gamesessions, many=True))
        data = GameSessionSerializer(gamesessions, many=True).data
        # print('gamesessionview data', data)
        return Response({ 'gamesessions': data })


# https://stackoverflow.com/questions/55416471/how-to-resolve-assertionerror-accepted-renderer-not-set-on-response-in-django


@api_view(('PATCH',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# @csrf_exempt
def assoc_questions(self, gamesession_id):
    """Add questions to game session array when game is started"""
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    #Grab the game session
    gamesession = GameSession.objects.get(id=gamesession_id)
    # grab all questions
    all_questions = list(Question.objects.all())
    # Take a random sample of the questions
    random_questions= random.sample(all_questions, 5)    
    # If the game already has questions, don't add them
    # If the game does not have questions, add them in one by one
    if gamesession.questions.count() == 0:
        for question in random_questions:
            gamesession.questions.add(question.id)
    # Serialize the game session
    data = GameSessionSerializer(gamesession).data
    # Send it back to the client
    return Response({ 'gamesession': data })
