# Generated by Django 4.1.7 on 2023-03-13 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_gamesession_session_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='role',
            field=models.CharField(choices=[('h', 'Host'), ('p1', 'Player One'), ('p2', 'Player Two'), ('p3', 'Player Three'), ('na', 'Empty')], default='na', max_length=2),
        ),
    ]