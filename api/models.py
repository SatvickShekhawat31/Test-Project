from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ops', 'Ops User'),
        ('client', 'Client User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"


class UploadedFile(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.uploader.username}"
