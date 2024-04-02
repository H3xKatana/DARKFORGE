from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .models import user

@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=user)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()