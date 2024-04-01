from django.db import models
from users.models import user
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
import os,uuid



User = get_user_model()
STATUS_CHOICES = (
    ('process', 'Processing'),
    ('deliverd', 'Delivered'),
)

STATUS = (
    ("draft", 'Draft'),
    ('disabled', 'Disabled'),
    ('coming_soon', 'Coming_Soon'),
    ('published', 'published')
)

RATING_CHOICES = (  
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Developers(models.Model):
    user   = models.ManyToManyField(User)
    active =models.BooleanField(default=True)
    def __str__(self):
        return f"Developer {self.pk}"
    





   
    
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default='',blank=True)
    image = models.ImageField(null=True,upload_to="image_uploads"
                                ,blank=True,default = 'image_uploads\placeholder.png' )
    url = models.URLField(unique=True)
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    price = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    platform = models.CharField(max_length=50)
    genres = models.ManyToManyField(Genre)
    is_published = models.BooleanField(default=True)
    youtube_video_url = models.URLField(blank=True, null=True)
    game_status = models.CharField(choices=STATUS, max_length=12, default='coming_soon')
    def __str__(self):
        return self.title


class GamesImages(models.Model):
    image = models.ImageField(upload_to='game_profile_pics/', null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.game)






class Rating(models.Model):
    game   = models.ForeignKey(Game, on_delete=models.CASCADE)
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1,validators=[MaxValueValidator(5)],null=False)
    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
    
class Comments(models.Model):
    game  = models.ForeignKey(Game, on_delete=models.CASCADE)
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=512)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
#############################3
class Wishlist(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class MyGames(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class FavoriteGames(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

###############################