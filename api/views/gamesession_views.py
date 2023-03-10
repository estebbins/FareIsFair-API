from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication
from rest_framework import status, generics
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import random

from ..serializers import UserSerializer, GameSessionSerializer, GameSessionCreateEditSerializer, PlayerAddSerializer
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
            # ! probably change this serializer!
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

@api_view(('POST',))
@permission_classes(())
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def sms(request):
    # sms <QueryDict: {'ToCountry': ['US'], 'ToState': [''], 'SmsMessageSid': ['SM3a74a337c65cce82f0985c7a7870ee33'], 'NumMedia': ['0'], 'ToCity': [''], 'FromZip': ['37217'], 'SmsSid': ['SM3a74a337c65cce82f0985c7a7870ee33'], 'FromState': ['TN'], 'SmsStatus': ['received'], 'FromCity': ['NASHVILLE'], 'Body': ['Test'], 'FromCountry': ['US'], 'To': ['+18442384011'], 'ToZip': [''], 'NumSegments': ['1'], 'MessageSid': ['SM3a74a337c65cce82f0985c7a7870ee33'], 'AccountSid': ['ACc113b237db9aa6a54522809d744a21f0'], 'From': ['+16155940171'], 'ApiVersion': ['2010-04-01']}>

    authentication_classes=()
    permission_classes=()
    print('sms', request.data)
    return Response({ 'sms': request.data })


@api_view(('PATCH',))

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# @csrf_exempt
def assoc_questions(request, gamesession_id):
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

@api_view(('PATCH',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# @csrf_exempt
def assoc_players(request):
    """Add questions to game session array when game is started"""
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    print('assocplayer req', request)
    print('players', request.data)
    #Grab the game session
    gamesession = GameSession.objects.get(id=request.data['gamesession_id'])
    print('gamesession', gamesession.__dict__)
    # grab the host
    host = User.objects.get(id=request.data['players']['host']['user']['id'])
    host_object =  UserSerializer(data=host)
    host_player = PlayerAddSerializer({'player': host_object}, {'game': GameSessionSerializer(gamesession.__dict__)})
    if host_player.is_valid():
        print('it is valid!', host_player)
        created_host_player = PlayerAddSerializer(data=host_object)
        if created_host_player.is_valid():
            created_host_player.save()
            return Response()
        else:
            print('created_hostplayer errors', created_host_player.errors)
            return Response(created_host_player.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('host_player error', host_player.errors)
        return Response(host_player.errors, status=status.HTTP_400_BAD_REQUEST)

    host_to_print = Player.objects.get(game_id=gamesession.id)
    print('hosttoprint', host_to_print) 

    # If there's data in player_one, then grab the user associated with the email
    if request.data['players']['player_one']:
        player_one = User.objects.get(email=request.data['players']['player_one'])
        print('playerone', player_one)
        PlayerAddSerializer(player=player_one, game=gamesession, role='p1')
    
    player_to_print = Player.objects.get(game=gamesession)
    print('playertoprint', player_to_print) 

    # If theres data in player_two, but not player one, make that player one
    if request.data['players']['player_two'] and not player_one:
        player_one = User.objects.get(email=request.data['players']['player_two'])
        Player(player=player_one, game=gamesession, role='p1')
       
    #else if there's a player one, then make player two, player two
    elif request.data['players']['player_two']:
        player_two = User.objects.get(email=request.data['players']['player_two'])
        Player(player=player_two, game=gamesession, role='p2')

    #If there's data in player_three but not one or two, make them player one
    if request.data['players']['player_three'] and not player_one and not player_two:
        player_one = User.objects.get(email=request.data['players']['player_three'])
        Player(player=player_one, game=gamesession, role='p1')
    #If there's data in player_three and there's not already a player two, make them 2
    elif request.data['players']['player_three'] and not player_two:
        player_two = User.objects.get(email=request.data['players']['player_three'])
        Player(player=player_two, game=gamesession, role='p2')
    elif request.data['players']['player_three']:
        player_three = User.objects.get(email=request.data['players']['player_three'])
        Player(player=player_three, game=gamesession, role='p3')

    # Serialize the game session
    data = GameSessionSerializer(gamesession).data
    # Send it back to the client
    return Response({ 'gamesession': data })

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def find_players(request, email):
    print('filter', email)
    users = User.objects.filter(email__startswith=email)

    data = UserSerializer(users, many=True).data

    return Response({ 'users': data })





