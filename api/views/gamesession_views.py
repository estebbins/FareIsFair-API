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

from ..serializers import UserSerializer, UserRegisterSerializer,  ChangePasswordSerializer, GameSessionSerializer, GameSessionCreateEditSerializer
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
    
class GameSessionCreate(generics.CreateAPIView):
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    # Serializer classes are required for endpoints that create data
    serializer_class = GameSessionCreateEditSerializer

    def post(self, request):
        # Pass the request data to the serializer to validate it
        print('request', request.data)

        gamesession = GameSessionCreateEditSerializer(data=request.data['gamesession'])

        print('gamesession in create', gamesession)
        # If that data is in the correct format...
        if gamesession.is_valid():
            created_gamesession = GameSessionCreateEditSerializer(data=gamesession.data)
            print('created_gamesession', created_gamesession)
            if created_gamesession.is_valid():

                # Save the user and send back a response!
                created_gamesession.save()
                return Response({ 'gamesession': created_gamesession.data }, status=status.HTTP_201_CREATED)
            else:
                print('created_gamesession', created_gamesession.errors)
                return Response(created_gamesession.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('gamesessionerror', gamesession.errors)
            return Response(gamesession.errors, status=status.HTTP_400_BAD_REQUEST)

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
