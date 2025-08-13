from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from users.choices import ROLE_CHOICES
from users.managers import UserManager


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        if self.first_name:
            return self.first_name + " " + self.last_name
        return self.username 