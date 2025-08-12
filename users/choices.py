

from django.db import models
from django.utils.translation import gettext as _


class ROLE_CHOICES(models.TextChoices):
    DRIVER = 'driver', _('Driver')
    ADMIN = 'admin', _('Admin')
