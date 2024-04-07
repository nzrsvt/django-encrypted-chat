from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class Profile(AbstractUser):
    last_seen = models.DateTimeField(null=True, blank=True)

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save()
