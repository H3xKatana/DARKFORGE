from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image
from os import path


def get_profile_picture_filepath(instance, filename):
    filename = filename.split('.')[-1]
    return path.join('profile_images', '{}profile_image.{}'.format(instance.pk, filename))


class user(AbstractUser):
    profile_picture = models.ImageField(
        _('profile picture'), upload_to=get_profile_picture_filepath, null=True, blank=True)
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    short_bio = models.TextField(_('Short Bio'), max_length=250, blank=True)
    source = models.CharField(_('source'), max_length=50, blank=True)
    


class OtpCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
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
        ('fady','Fady')
    ], blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    