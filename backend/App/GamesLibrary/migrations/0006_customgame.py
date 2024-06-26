# Generated by Django 4.0.1 on 2024-04-12 16:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GamesLibrary', '0005_rename_product_cartitem_game_game_discounts_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('userTechLevel', models.CharField(choices=[('beginner ', 'beginner'), ('entry level', 'entry level'), ('junior level', 'junior level'), ('senior level', 'senior level')], default='beginner', max_length=25)),
                ('game_complexity', models.CharField(choices=[('fast game ', 'fast game'), ('entry level', 'entry level'), ('mideum game ', 'mideum game '), ('AA //  Big Game Project', 'Big Game Project'), ('AAA level ', 'AAA level ')], default='fast game', max_length=25)),
                ('generalinfo', models.TextField(blank=True, default='')),
                ('platform', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='custom_game/')),
                ('progression', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('game_status', models.CharField(choices=[('draft', 'Draft'), ('Lore design', 'lore design'), ('charachters desgin', 'charachters desgin'), ('Graphics Desgin', 'Graphics Desgin'), ('adding sounds', 'adding sounds'), ('Game UI', 'Game UI'), ('testing ', 'testing '), ('published soon', 'published soon'), ('Game is ready', 'Game ready')], default='Draft', max_length=20)),
                ('genres', models.ManyToManyField(to='GamesLibrary.Genre')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
