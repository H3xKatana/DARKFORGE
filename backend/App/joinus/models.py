from django.db import models
from users.models import user
class CV(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='cv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV for {self.user.username}"
