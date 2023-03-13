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
from django.utils import timezone

from ..serializers import UserSerializer, GameSessionSerializer, GameSessionCreateEditSerializer, PlayerSerializer, PlayerResponseSerializer, PlayerSerializer, QuestionSerializer
from ..models.user import User
from ..models.game_session import GameSession, Player, Question, PlayerResponse

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
    print('count', gamesession.questions.count())
    if gamesession.questions.count() == 0:
        for question in random_questions:
            gamesession.questions.add(question.id)
    print('questions', gamesession.questions.values_list('id'))
    # Grab the questions associated with the game to send back in the response
    game_questions = Question.objects.filter(id__in=gamesession.questions.values_list('id')).distinct()
    # Grab the players associated with the game to send back in the response
    game_players = Player.objects.filter(game=gamesession_id).distinct()
    # game_players_two = Player.objects.get(game=gamesession_id)
    # print(game_players_two)
    game_users = User.objects.filter(id__in=gamesession.players.values_list('id')).distinct()
    # Serialize the data
    game_data = GameSessionSerializer(gamesession).data
    question_data = QuestionSerializer(game_questions, many=True).data
    player_data = PlayerSerializer(game_players, many=True).data
    print('qd', question_data)
    user_data = UserSerializer(game_users, many=True).data
    # Send it back to the client
    return Response({ 'gameSession': game_data, 'gameQuestions': question_data, 'players': player_data, 'users': user_data })

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
    users = User.objects.filter(email__startswith=email).distinct()

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

    if active_game.game_result == 'completed':
        current_question = None
        delta = None
    else:
        try:
            current_question = Question.objects.get(id=active_game.active_question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            delta = float(current_question.answer) - float(request.data['Body'])
        except ValueError or TypeError:
            delta = -1
    # Compare responses
    print('current question answer', float(current_question.answer))
    print('body', float(request.data['Body']))

    print('delta', delta)
    print('question in sms', current_question)

    try: 
        created_player_response = PlayerResponse.objects.get(question=current_question, player=player, game=active_game)
        created_player_response.sms_sid=request.data['SmsSid']
        created_player_response.response=request.data['Body']
        created_player_response.to=request.data['To']
        created_player_response.from_num=request.data['From']
        created_player_response.msg_sid=request.data['MessageSid']
        created_player_response.delta=delta
    except PlayerResponse.DoesNotExist:
        created_player_response = PlayerResponse.objects.create(
            sms_sid=request.data['SmsSid'], 
            response=request.data['Body'],
            to=request.data['To'],
            from_num=request.data['From'],
            msg_sid=request.data['MessageSid'],
            question=current_question,
            player=player,
            game=active_game,
            delta=delta
        )

    created_player_response.save()
    
    print('created_player_response', created_player_response)

    return Response(status=status.HTTP_201_CREATED)

# @api_view(('GET',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def find_responses(request):

class PlayerResponseIndex(generics.ListAPIView):
    """View to return player responses for the specific question"""
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    serializer_class = PlayerResponseSerializer

    def get(self, request, gamesession_id, question_id):
        """Index request"""
        # Get all the responses that match the game Id & the question Id
        responses = PlayerResponse.objects.filter(game=gamesession_id, question=question_id).distinct()
        print('Index Responses', responses)
        # Run the data through the serializer
        data = PlayerResponseSerializer(responses, many=True).data
        print('PlayerResponseIndex data', data)
        return Response({ 'player_responses': data })

class QuestionDetail(generics.ListAPIView):
    """View to return question detail"""
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get(self, request, question_id):
        """Detail request"""
        # Get all the responses that match the game Id & the question Id
        question = Question.objects.get(id=question_id)
        print('Question Detail', question)
        # Run the data through the serializer
        data = QuestionSerializer(question).data
        print('QuestionIndex data', data)
        return Response({ 'question_detail': data })

@api_view(('PATCH',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def begin_game(request, gamesession_id):
    # Grab the game session
    game_session = GameSession.objects.get(id=gamesession_id)
    # Randomly select the first question
    print(game_session.__dict__)
    print('2nd option', game_session.questions.values_list('id'))
    question_ids = game_session.questions.values_list('id', flat=True)
    first_question = random.sample(list(question_ids), 1) 
    # Update the game session to active, in progress, and modify the play date to now
    print('fq', first_question[0])
    print(game_session.questions)
    game_session.is_active=True
    game_session.game_result='in_progress'
    game_session.played_date=timezone.now().date()
    game_session.active_question=Question.objects.get(id=first_question[0])
    game_session.save()
    # game_session.update(is_active=True, game_result='in_progress', played_date=timezone.now(), active_question=first_question)
    # Serialize the data
    game_data = GameSessionSerializer(game_session).data
    return Response({ 'gameSession': game_data })

@api_view(('PATCH',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def score_player(request):
    print('score player', request.data)
    player = Player.objects.get(player=request.data["player_id"], game=request.data["game_session_id"])
    player.score = request.data["score"] + player.score
    player.save()
    players = Player.objects.filter(game=request.data["game_session_id"])
    player_data = PlayerSerializer(players, many=True).data
    return Response({ 'playerData': player_data })

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def next_round(request, gamesession_id, question_id):
    GameSession.objects.get(id=gamesession_id).questions.remove(question_id)
    game_session = GameSession.objects.get(id=gamesession_id)
    # Randomly select the first question
    # print(game_session.__dict__)
    # print('2nd option', game_session.questions.values_list('id', flat=True))
    question_ids = game_session.questions.values_list('id', flat=True)
    if len(question_ids) == 0:
        game_session.game_result='completed'
        game_session.save()
        game_data = GameSessionSerializer(game_session).data
        return Response({ 'gameSession': game_data })
    else:
        next_question = random.sample(list(question_ids), 1) 
        game_session.active_question=Question.objects.get(id=next_question[0])
        game_session.save()
        game_data = GameSessionSerializer(game_session).data
        return Response({ 'gameSession': game_data })
    # Update the game session to active, in progress, and modify the play date to now
    # print('fq', first_question[0])
    # print(game_session.questions)
    
    # game_session.update(is_active=True, game_result='in_progress', played_date=timezone.now(), active_question=first_question)
    # Serialize the data
    
    # return Response({ 'gameSession': game_data })

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def game_detail(request, gamesession_id):
    gamesession = GameSession.objects.get(id=gamesession_id)
    game_questions = Question.objects.filter(id__in=gamesession.questions.values_list('id')).distinct()
    # Grab the players associated with the game to send back in the response
    game_players = Player.objects.filter(game=gamesession_id).distinct()
    # game_players_two = Player.objects.get(game=gamesession_id)
    # print(game_players_two)
    game_users = User.objects.filter(id__in=gamesession.players.values_list('id')).distinct()
    # Serialize the data
    game_data = GameSessionSerializer(gamesession).data
    question_data = QuestionSerializer(game_questions, many=True).data
    player_data = PlayerSerializer(game_players, many=True).data
    print('qd', question_data)
    user_data = UserSerializer(game_users, many=True).data
    # Send it back to the client
    return Response({ 'gameSession': game_data, 'gameQuestions': question_data, 'players': player_data, 'users': user_data })

# @api_view(('DELETE',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def game_delete(request, id):
#     gamesession = GameSession.objects.get(pk=id)
#     if gamesession.game_result == 'pending':
#         gamesession.delete()

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[ SessionAuthentication ]
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk):
        """Show request"""
        game = get_object_or_404(GameSession, pk=pk)
        # Only want to show owned mangos?
      
        # Run the data through the serializer so it's formatted
        data = GameSessionSerializer(game).data
        return Response({ 'mango': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate game to delete
        game = get_object_or_404(GameSession, pk=pk)
        if game.game_result == 'pending':
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        raise PermissionDenied('Unauthorized, unable to delete game if result is not pending')


