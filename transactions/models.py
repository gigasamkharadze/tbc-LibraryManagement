from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Borrower


class Transaction(models.Model):
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE, related_name='transactions', verbose_name=_('book'))
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='transactions', verbose_name=_('borrower'))
    checkout_date = models.DateField(verbose_name=_('checkout date'))
    return_date = models.DateField(verbose_name=_('return date'), blank=True, null=True)

    def __str__(self):
        return f'{self.book} - {self.borrower}'

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        ordering = ['-checkout_date']