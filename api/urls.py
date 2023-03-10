from django.urls import path
# from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.gamesession_views import GameSessions, assoc_questions, assoc_players, find_players, GameSessionCreate

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
    path('find_players/<str:email>', find_players, name='find_players')
]
