# Generated by Django 4.1.7 on 2023-03-09 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('screenname', models.CharField(max_length=25, unique=True)),
                ('phone_number', models.CharField(max_length=12)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('session_code', models.CharField(default='b94dab', editable=False, max_length=6)),
                ('session_password', models.CharField(max_length=8)),
                ('game_result', models.CharField(choices=[('completed', 'Completed'), ('abandoned', 'Abandoned'), ('in_progress', 'In Progress'), ('pending', 'Pending')], default='pending', max_length=11)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('played_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('h', 'Host'), ('p1', 'Player One'), ('p1', 'Player Two'), ('p1', 'Player Three'), ('na', 'Empty')], default='na', max_length=2)),
                ('score', models.IntegerField(default=0)),
                ('winner', models.BooleanField(null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gamesession')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gamesession',
            name='players',
            field=models.ManyToManyField(through='api.Player', to=settings.AUTH_USER_MODEL),
        ),
    ]
