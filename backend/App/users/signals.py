from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .models import user,Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings




@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=user)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        recipient_email = instance.recipient.email
        subject = 'New Notification'
        html_message = render_to_string('email/notification_email.html', {'notification': instance})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_message, from_email, [recipient_email], html_message=html_message)