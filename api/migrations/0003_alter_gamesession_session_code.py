# Generated by Django 4.1.7 on 2023-03-08 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_gamesession_played_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='session_code',
            field=models.CharField(default='37749e', editable=False, max_length=6),
        ),
    ]
