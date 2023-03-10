# Generated by Django 4.1.7 on 2023-03-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_gamesession_session_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=1000)),
                ('additional', models.CharField(max_length=1000)),
                ('image', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=1000)),
            ],
        ),
    ]