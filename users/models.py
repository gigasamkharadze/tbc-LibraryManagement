from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from library.models import Book
from users.choices import PositionChoices


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('profile', 3)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, verbose_name=_('first name'))
    last_name = models.CharField(max_length=30, verbose_name=_('last name'))
    email = models.EmailField(unique=True, verbose_name=_('email'))
    personal_number = models.CharField(max_length=11, unique=True, verbose_name=_('personal number'))
    birth_date = models.DateField(verbose_name=_('birth date'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('staff'))

    class UserProfile(models.IntegerChoices):
        LIBRARIAN = 1, _('Librarian')
        BORROWER = 2, _('Borrower')
        ADMIN = 3, _('Admin')

    profile = models.IntegerField(choices=UserProfile.choices, default=UserProfile.LIBRARIAN, verbose_name=_('profile'))

    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'personal_number', 'birth_date']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian_profile', verbose_name=_('user'))
    position = models.CharField(max_length=2, choices=PositionChoices.choices, verbose_name=_('position'))
    description = models.TextField(verbose_name=_('description'))
    photo = models.ImageField(upload_to='librarian_photos', blank=True, null=True, verbose_name=_('photo'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = _('librarian profile')
        verbose_name_plural = _('librarian profiles')


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='borrower_profile', verbose_name=_('user'))
    borrowed_books = models.ManyToManyField(Book, related_name='borrowed_books', verbose_name=_('borrowed books'))
    photo = models.ImageField(upload_to='borrower_photos', blank=True, null=True, verbose_name=_('photo'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = _('borrower profile')
        verbose_name_plural = _('borrower profiles')
