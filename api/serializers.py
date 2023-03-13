from django.contrib.auth import get_user_model
from rest_framework import serializers

# from .models.mango import Mango
from .models.user import User
from .models.game_session import GameSession, Player, Question, PlayerResponse

# class MangoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Mango
#         fields = ('id', 'name', 'color', 'ripe', 'owner')

class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = (
            'id', 
            'is_active', 
            'session_name', 
            'questions',
            'players',
            'game_result',
            'created_date',
            'played_date',
            'active_question'
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id', 
            'prompt',
            'additional',
            'image',
            'answer'
        )

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id', 
            'player',
            'game',
            'role',
            'score', 
            'winner'
        )

class PlayerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerResponse
        fields = (
            'id',
            'game',
            'player',
            'question',
            'sms_sid',
            'response',
            'to',
            'from_num',
            'msg_sid',
            'delta'
        )

class GameSessionCreateEditSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    is_active = serializers.BooleanField(required=True)
    session_name = serializers.CharField(max_length=25, required=False)
    # session_password = serializers.CharField(max_length=10, required=True)
    questions = QuestionSerializer(many=True, required=False)
    players = PlayerSerializer(many=True, required=False)
    game_result = serializers.CharField(max_length=11, required=False)
    created_date = serializers.DateField(required=False)
    played_date = serializers.DateField(required=False)

    def create(self, validated_data):
        return GameSession.objects.create(**validated_data)



class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'player', 
            'game',
            'role',
            'score',
            'winner'
        )

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'screenname', 'phone_number', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    screenname = serializers.CharField(max_length=300, required=True)
    phone_number = serializers.CharField(max_length=12, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)


class PlayerAddSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    game = GameSessionSerializer(required=False)
    player = UserSerializer(required=False)
    role = serializers.CharField(max_length=2, required=True)
    score = serializers.IntegerField(required=False)
    winner = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Player.objects.create(**validated_data)
    
class PlayerAddResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    game = GameSessionSerializer(required=False)
    player = UserSerializer(required=False)
    question = QuestionSerializer(required=False)
    sms_sid = serializers.CharField(max_length=100, required=False)
    response = serializers.CharField(max_length=1000, required=False)
    to = serializers.CharField(max_length=100, required=False)
    from_num = serializers.CharField(max_length=100, required=False)
    msg_sid = serializers.CharField(max_length=100, required=False)
    delta = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)

    def create(self, validated_data):
        return PlayerResponse.objects.create(**validated_data)


