# Generated by Django 4.0.1 on 2024-04-28 09:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GamesLibrary', '0025_customgame_order_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgame',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='mygames',
            unique_together={('user', 'game')},
        ),
    ]
