from django.db import models
from django.contrib.auth import get_user_model
from . import User
import uuid

class Question(models.Model):
    prompt = models.CharField(max_length=1000)
    additional = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        # This must return a string
        return f"{self.prompt}"


class GameSession(models.Model):
    # This field is toggeled to True when the game is in progress ONLY
    is_active = models.BooleanField(default=False)
    # Universally unique identifier field up to 6 characters
    def session_name_default():
        return uuid.uuid4().hex[:6]
    
    session_name = models.CharField(max_length=20, default=session_name_default)
    
    # session_code = models.CharField(
    #         max_length=6,
    #         default = session_code_default
    # )

    # Password set by host to log into game
    # session_password = models.CharField(max_length=8)
    # ! Questions join - Figure out limiting to specific #
    questions = models.ManyToManyField(Question, blank=True)
    # ! Responses join - not sure if necessary

    # https://www.youtube.com/watch?v=-HuTlmEVOgU 
    # Players & Player Data 
    players = models.ManyToManyField(get_user_model(), through='Player', blank=True)

    #### Game Data ####
    # Overall Game Result
    GAME_RESULT_CHOICES = (
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending')
    )
    game_result = models.CharField(
        max_length=11, 
        choices=GAME_RESULT_CHOICES, 
        default='pending'
    )

    # Date the game was created (not editable, set upon creation of object)
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    # Date the game was completed (will be set at the end of the game)
    played_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    active_question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL, related_name="active_question")


    def __str__(self):
        # This must return a string
        return f"The game code is named '{self.session_name}'"
    





# # Create your models here.
# class Mango(models.Model):
#   # define fields
#   # https://docs.djangoproject.com/en/3.0/ref/models/fields/
#   name = models.CharField(max_length=100)
#   ripe = models.BooleanField()
#   color = models.CharField(max_length=100)
#   owner = models.ForeignKey(
#       get_user_model(),
#       on_delete=models.CASCADE
#   )

#   def __str__(self):
#     # This must return a string
#     return f"The mango named '{self.name}' is {self.color} in color. It is {self.ripe} that it is ripe."

#   def as_dict(self):
#     """Returns dictionary version of Mango models"""
#     return {
#         'id': self.id,
#         'name': self.name,
#         'ripe': self.ripe,
#         'color': self.color
#     }

### Connection between Users & Game Sessions ###
class Player(models.Model):
    # Grab the user & game session
    player = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    game = models.ForeignKey(GameSession, on_delete=models.CASCADE, blank=True)
    # Set up role options for the players
    ROLE_CHOICES = (
        ('h', 'Host'),
        ('p1', 'Player One'),
        ('p1', 'Player Two'),
        ('p1', 'Player Three'),
        ('na', 'Empty')
    )
    # Define the role, default to 'na'
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='na')
    # Create a field for the game score
    score = models.IntegerField(default=0)
    # Track if the player won the game (true) or lost(false) or game has not concluded (null)
    winner = models.BooleanField(null=True)

    def __str__(self):
        # This must return a string
        return f"This player is the '{self.role}'"

class PlayerResponse(models.Model):
    sms_sid = models.CharField(max_length=100)
    response = models.CharField(max_length=1000)
    to = models.CharField(max_length=100)
    from_num = models.CharField(max_length=100)
    msg_sid = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(GameSession, on_delete=models.SET_NULL, null=True)
    delta = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def __str__(self):
        # This must return a string
        return f"{self.player}'s answer: {self.response}"



