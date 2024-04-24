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
from django.db.models import Q



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
    image = models.ImageField(default='default.jpg', upload_to='genres_pics')

    def __str__(self):
        return self.name

class Platforms(models.Model):
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
    game_requirments = models.TextField(default='',blank=True)
    image = models.ImageField(default='default.jpg', upload_to='game_pics')
    url = models.URLField(unique=True)
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    price = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    genres = models.ManyToManyField(Genre)
    platforms = models.ManyToManyField(Platforms)
    discounts = models.IntegerField(default=0,validators=[MaxValueValidator(50)],null=False)
    is_published = models.BooleanField(default=True)
    youtube_video_url = models.URLField(blank=True, null=True)
    game_status = models.CharField(choices=STATUS, max_length=12, default='coming_soon')
    rate =models.FloatField(default=0, validators = [MinValueValidator(0.0),MaxValueValidator(5.0)])

    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def is_recent(self):
        # Calculate the difference between now and the creation date
        time_difference = timezone.now() - self.created_at
        # Check if the difference is less than or equal to 10 days
        return time_difference.days <= 10
    

   
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

class MyGames(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class FavoriteGames(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'game')
###############################

    ############################33
# Improving Custom Status Choices
CUSTOM_STATUS_CHOICES = (
    ("draft", "Draft"),
    ("concept", "Concept"),
    ("prototyping", "Prototyping"),
    ("alpha", "Alpha Version"),
    ("beta", "Beta Version"),
    ("playtesting", "Playtesting"),
    ("polishing", "Polishing"),
    ("final_testing", "Final Testing"),
    ("marketing", "Marketing"),
    ("launch", "Launch"),
    ("post_launch_support", "Post-launch Support"),
)

# Improving Complexity Choices
COMPLEXITY_CHOICES = (
    ("fast_game", "Fast Game"),
    ("entry_level", "Entry Level"),
    ("medium_game", "Medium Game"),
    ("big_game_project", "Big Game Project"),
    ("aaa_level", "AAA Level"),
)

# Improving Tech Level Choices
TECH_LEVEL_CHOICES = (
    ("beginner", "Beginner"),
    ("entry_level", "Entry Level"),
    ("junior_level", "Junior Level"),
    ("senior_level", "Senior Level"),
)

class CustomGame(models.Model):
    user     = models.ForeignKey(user, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=100)
    user_tech_level = models.CharField(choices=TECH_LEVEL_CHOICES, max_length=25, default="beginner")
    game_complexity = models.CharField(choices=COMPLEXITY_CHOICES, max_length=25, default="fast_game")
    general_info = models.TextField(default="", blank=True)
    platform = models.CharField(max_length=50)
    Platforms = models.ManyToManyField(Platforms)
    genres = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to="custom_game/", null=True, blank=True)
    progression = models.IntegerField(default=0, validators=[MaxValueValidator(100)], null=False)
    game_status = models.CharField(choices=CUSTOM_STATUS_CHOICES, max_length=20, default="draft")
    prototype = models.BooleanField(default=False)
    prototype_game = models.FileField(upload_to="prototype_games/", null=True, blank=True)
    prototype_video_url = models.URLField(blank=True, null=True)
    payment= models.BooleanField(default=False)
    price = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    order_reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    @property
    def is_recent(self):
        # Calculate the difference between now and the creation date
        time_difference = timezone.now() - self.created_at
        # Check if the difference is less than or equal to 10 days
        return time_difference.days <= 10
    def __str__(self):
        return f"{self.user.username} - {self.title}"





class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    order_reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

    @property
    def total(self):
        return sum(item.quantity * item.price for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price(self):
        discount_percentage = self.game.discounts
        discount_decimal = (100 - discount_percentage) / 100
        discounted_price = self.game.price * discount_decimal
        return discounted_price

    def __str__(self):
        return f"{self.quantity} x {self.game.title} in order #{self.order.id}"
    

    def remove_from_cart(self):
        self.delete()









class UserPayment(models.Model):
	app_user = models.ForeignKey(user, on_delete=models.CASCADE)
	payment_bool = models.BooleanField(default=False)
	stripe_checkout_id = models.CharField(max_length=500)


@receiver(post_save, sender=user)
def create_user_payment(sender, instance, created, **kwargs):
	if created:
		UserPayment.objects.create(app_user=instance)