# Generated by Django 4.1.7 on 2023-03-11 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_player_game_alter_player_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesession',
            name='active_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_question', to='api.question'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_sid', models.CharField(max_length=100)),
                ('response', models.CharField(max_length=1000)),
                ('to', models.CharField(max_length=100)),
                ('from_num', models.CharField(max_length=100)),
                ('msg_sid', models.CharField(max_length=100)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.question')),
            ],
        ),
    ]
