from django.db import models
from django.utils.translation import gettext_lazy as _


class PositionChoices(models.TextChoices):
    HEAD_LIBRARIAN = 'HL', _('Head Librarian')
    ASSISTANT_LIBRARIAN = 'AL', _('Assistant Librarian')
    LIBRARY_ASSISTANT = 'LA', _('Library Assistant')
