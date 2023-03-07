from django.db import models
from django.contrib.auth import get_user_model
from . import User
import uuid

class GameSession(models.Model):
    # This field is toggeled to True when the game is in progress ONLY
    is_active = models.BooleanField(default=False)
    # Universally unique identifier field up to 6 characters
    session_code = models.UUIDField(
            primary_key = True,
            default = uuid.uuid4().hex[:6],
            editable = False
    )
    # Password set by host to log into game
    session_password = models.CharField(max_length=8)
    # ! Questions join - Figure out limiting to specific #
    # questions = models.ManyToManyField(Question)
    # ! Responses join - not sure if necessary

    #### Player Data####
    host = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL
        # Don't want to delete games when users get deleted because they could be in other accounts
        #on_delete=models.CASCADE
    )
    player_one = models.ForeignKey(
        # Do I need anything else here?
        User,
        on_delete=models.SET_NULL
    )
    player_two = models.ForeignKey(#
        # Do I need anything else here?
        User,
        on_delete=models.SET_NULL
    )
    player_three = models.ForeignKey(
        # Do I need anything else here?
        User,
        on_delete=models.SET_NULL
    )
    # Fields to hold scores
    host_score = models.IntegerField()
    player_one_score = models.IntegerField()
    player_two_score = models.IntegerField()
    player_three_score = models.IntegerField()

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
    winner = models.ForeignKey(
        # How do I plug in the user here?
        get_user_model(),
        on_delete=models.SET_NULL
    )
    # Date the game was created (not editable, set upon creation of object)
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    # Date the game was completed (will be set at the end of the game)
    played_date = models.DateField(auto_now=False, auto_now_add=False)

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
