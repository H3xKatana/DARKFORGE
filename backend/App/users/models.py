from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os import path


def get_profile_picture_filepath(instance, filename):
    filename = filename.split('.')[-1]
    return path.join('profile_images', '{}profile_image.{}'.format(instance.pk, filename))


class user(AbstractUser):
    
    source = models.CharField(_('source'), max_length=50, blank=True)
    


class OtpCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    source = models.CharField(_('source'), max_length=50, blank=True)
    def __str__(self):
        return self.code

class Profile(models.Model):
    # to inhirate from the user model / on_del if the user the profile is deleted the rev is not true 
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    banner = models.ImageField(default='defualt.jpg',upload_to='profile_banners')
    bio = models.TextField(_('Bio'), max_length=250, blank=True)
    short_bio = models.TextField(_('Short Bio'), max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('fady','Fady'),
        
    ], blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"
    

class Notification(models.Model):
    recipient = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.message