from django.db import models
from django.utils.translation import gettext_lazy as _
from library.models import Book
from users.models import Borrower
from reservations.choices import StatusChoices


class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'), related_name='reservations')
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, verbose_name=_('Borrower'),
                                 related_name='reservations')
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE, verbose_name=_('Status'))

    def __str__(self):
        return f'{self.book} - {self.borrower}'

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')
        ordering = ['-date']
