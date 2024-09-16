from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.CharField(max_length=150, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.username
        super().save(*args, **kwargs)
