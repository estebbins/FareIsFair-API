from django.urls import path
# from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.gamesession_views import GameSessions, assoc_questions, assoc_players, find_players, sms, begin_game, score_player, next_round, game_detail, QuestionDetail, PlayerResponseIndex, GameSessionCreate, GameDetail

urlpatterns = [
  	# Restful routing
    # path('mangos/', Mangos.as_view(), name='mangos'),
    # path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('', GameSessions.as_view(), name='home'),
    path('games/new/', GameSessionCreate.as_view(), name='gamesession_create'),
    path('games/add_questions/<int:gamesession_id>/', assoc_questions, name='add_questions'),
    path('games/add_players/', assoc_players, name='add_players'),
    path('find_players/<str:email>', find_players, name='find_players'),
    # URL for Twilio Webhook
    path('sms/', sms, name='sms'),
    # URLs for Live Games
    path('livegame/question/<int:question_id>/', QuestionDetail.as_view(), name='get_question'),
    path('livegame/begin/<int:gamesession_id>/', begin_game , name='begin_game'),
    path('livegame/<int:gamesession_id>/<int:question_id>/', PlayerResponseIndex.as_view(), name='get_responses'),
    path('livegame/add_score/', score_player, name='score_player'),
    path('livegame/next_round/<int:gamesession_id>/<int:question_id>/', next_round, name='next_round'),
    # path('game/<int:gamesession_id>/', game_detail, name='game_detail' ),
    path('game/delete/<int:pk>/', GameDetail.as_view(), name='game_delete')
]
