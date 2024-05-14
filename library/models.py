from django.db import models
from django.utils.translation import gettext_lazy as _


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Genre name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('First name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last name'))
    date_of_birth = models.DateField(verbose_name=_('Date of birth'))
    date_of_death = models.DateField(verbose_name=_('Date of death'), null=True, blank=True)
    biography = models.TextField(verbose_name=_('Biography'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['last_name', 'first_name', 'date_of_birth']


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'), related_name='books')
    genre = models.ManyToManyField(Genre, verbose_name=_('Genre'), related_name='books')
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    publication_date = models.DateField(verbose_name=_('Publication date'))
    description = models.TextField(verbose_name=_('Description'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['title', 'publication_date', 'author', 'quantity']

