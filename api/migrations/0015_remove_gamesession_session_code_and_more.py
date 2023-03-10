# Generated by Django 4.1.7 on 2023-03-13 15:58

import api.models.game_session
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_playerresponse_delta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesession',
            name='session_code',
        ),
        migrations.RemoveField(
            model_name='gamesession',
            name='session_password',
        ),
        migrations.AddField(
            model_name='gamesession',
            name='session_name',
            field=models.CharField(default=api.models.game_session.GameSession.session_name_default, max_length=20),
        ),
    ]
