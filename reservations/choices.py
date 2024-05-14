from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.IntegerChoices):
    ACTIVE = 1, _('Active')
    INACTIVE = 2, _('Inactive')