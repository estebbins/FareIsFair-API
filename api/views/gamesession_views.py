from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication
from rest_framework import status, generics
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import random

from ..serializers import UserSerializer, GameSessionSerializer, GameSessionCreateEditSerializer, PlayerSerializer, PlayerAddSerializer, PlayerSerializer
from ..models.user import User
from ..models.game_session import GameSession, Player, Question, Player_Response

class GameSessions(generics.ListAPIView):
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    serializer_class = GameSessionSerializer
    def get(self, request):
        """Index request"""
        # Get all the games
        gamesessions = GameSession.objects.filter(players__in=[request.user.id]).distinct()
        print('gamesession', gamesessions)
        # Run the data through the serializer
        # print('gamesession(gamesessions)', GameSessionSerializer(gamesessions, many=True))
        data = GameSessionSerializer(gamesessions, many=True).data
        # print('gamesessionview data', data)
        players = Player.objects.filter(game__in=gamesessions).distinct()
        player_data = PlayerSerializer(players, many=True).data
        return Response({ 'gamesessions': data, 'playerdata': player_data })
    
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
                game = GameSession.objects.get(id=created_gamesession.data['id'])
                new_player = Player.objects.create(player=request.user, role='h', game=game)
                print('newplayer', new_player)
                print('created game session!!!!!', created_gamesession.data)
                return Response({ 'gamesession': created_gamesession.data }, status=status.HTTP_201_CREATED)
            else:
                print('created_gamesession', created_gamesession.errors)
                return Response(created_gamesession.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('gamesessionerror', gamesession.errors)
            return Response(gamesession.errors, status=status.HTTP_400_BAD_REQUEST)

# https://stackoverflow.com/questions/55416471/how-to-resolve-assertionerror-accepted-renderer-not-set-on-response-in-django
# https://stackoverflow.com/questions/22816704/django-get-a-random-object 


@api_view(('PATCH',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
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
    # host = User.objects.get(id=request.data['players']['host']['user']['id'])
    # host_player = Player.objects.create(role='h', game=gamesession, player=host)
    # print('hostplayer', host_player.__dict__)
    # host_object =  UserSerializer(data=host)
    # host_object = {
    #     'data': {
    #         # 'player': host.__dict__,
    #         # 'game': gamesession.__dict__,
    #         'role': 'h'
    #     }
    # }
    # print('host_object', host_object)
    # host_player = PlayerAddSerializer(data=host_object['data'])
    # if host_player.is_valid():
    #     print('it is valid!', host_player)
    #     created_host_player = PlayerSerializer(data=host_player.data)
    #     print('created host player', created_host_player)
    #     if created_host_player.is_valid():
    #         print('created host playerdata', created_host_player.validated_data)
    #         # created_host_player.data.add(gamesession)
    #         # created_host_player.add(host)
    #         print('created host data', created_host_player)
    #         created_host_player.save()
    #         # print('created host data', created_host_player)
    #         return Response()
    #     else:
    #         print('created_hostplayer errors', created_host_player.errors)
    #         return Response(created_host_player.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     print('host_player error', host_player.errors)
    #     return Response(host_player.errors, status=status.HTTP_400_BAD_REQUEST)

    # host_to_print = Player.objects.get(game_id=gamesession.id)
    # print('hosttoprint', host_to_print) 

    # If there's data in player_one, then grab the user associated with the email
    if request.data['players']['player_one']:
        player_one = User.objects.get(email=request.data['players']['player_one'])
        print('playerone', player_one)
        Player.objects.create(role='p1', game=gamesession, player=player_one)

    
    # player_to_print = Player.objects.get(game=gamesession)
    # print('playertoprint', player_to_print) 

    # If theres data in player_two, but not player one, make that player one
    if request.data['players']['player_two'] and not player_one:
        player_one = User.objects.get(email=request.data['players']['player_two'])
        Player.objects.create(role='p1', game=gamesession, player=player_one)
       
    #else if there's a player one, then make player two, player two
    elif request.data['players']['player_two']:
        player_two = User.objects.get(email=request.data['players']['player_two'])
        Player.objects.create(player=player_two, game=gamesession, role='p2')

    #If there's data in player_three but not one or two, make them player one
    if request.data['players']['player_three'] and not player_one and not player_two:
        player_one = User.objects.get(email=request.data['players']['player_three'])
        Player.objects.create(role='p1', game=gamesession, player=player_one)
    #If there's data in player_three and there's not already a player two, make them 2
    elif request.data['players']['player_three'] and not player_two:
        player_two = User.objects.get(email=request.data['players']['player_three'])
        Player.objects.create(player=player_two, game=gamesession, role='p2')
    elif request.data['players']['player_three']:
        player_three = User.objects.get(email=request.data['players']['player_three'])
        Player.objects.create(player=player_three, game=gamesession, role='p3')

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

@api_view(('POST',))
@permission_classes(())
@renderer_classes((JSONRenderer,))
@csrf_exempt
def sms(request):
    #Example
    # sms 
    # 
    # data = <QueryDict: {'ToCountry': ['US'], 'ToState': [''], 'SmsMessageSid': ['SM3a74a337c65cce82f0985c7a7870ee33'], 'NumMedia': ['0'], 'ToCity': [''], 'FromZip': ['37217'], 'SmsSid': ['SM3a74a337c65cce82f0985c7a7870ee33'], 'FromState': ['TN'], 'SmsStatus': ['received'], 'FromCity': ['NASHVILLE'], 'Body': ['Test'], 'FromCountry': ['US'], 'To': ['+15555555555'], 'ToZip': [''], 'NumSegments': ['1'], 'MessageSid': ['SM3a74a337c65cce82f0985c7a7870ee33'], 'AccountSid': ['ACc113b237db9aa6a54522809d744a21f0'], 'From': ['+15555555555'], 'ApiVersion': ['2010-04-01']}>
    
    authentication_classes=()
    permission_classes=()
    
    # If sms not from US, send bad_request
    if request.data['FromCountry'] not in 'US':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Try to find the player matching the phone number
    try:
        player = User.objects.get(phone_number=request.data['From'])
    except User.DoesNotExist:
        # Raise 400 error if user not found with a matching phone number
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    print('player in sms', player)

    # Try to find an active game with that player
    try:
        active_game = GameSession.objects.get(is_active=True, players=player.id)
    except GameSession.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    print('game in sms', active_game)

    try:
        current_question = Question.objects.get(id=active_game.active_question_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    print('question in sms', current_question)

    created_player_response = Player_Response.objects.create(
        sms_sid=request.data['SmsSid'], 
        response=request.data['Body'],
        to=request.data['To'],
        from_num=request.data['From'],
        msg_sid=request.data['MessageSid'],
        question=current_question,
        player=player,
        game=active_game
    )
    created_player_response.save()
    
    print('created_player_response', created_player_response)

    return Response(status=status.HTTP_201_CREATED)





