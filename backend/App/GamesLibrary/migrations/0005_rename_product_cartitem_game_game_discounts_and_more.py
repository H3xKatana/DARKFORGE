# Generated by Django 4.0.1 on 2024-04-10 16:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamesLibrary', '0004_cart_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='product',
            new_name='Game',
        ),
        migrations.AddField(
            model_name='game',
            name='discounts',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]