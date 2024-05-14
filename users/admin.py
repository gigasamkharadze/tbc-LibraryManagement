from django.contrib import admin
from users.models import User, Librarian, Borrower


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'personal_number', 'birth_date', 'is_active', 'is_staff', 'profile')
    list_filter = ('is_active', 'is_staff', 'profile')


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'description', 'photo')
    list_filter = ('position',)


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo')