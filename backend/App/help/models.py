from django.db import models
from users.models import user
# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'