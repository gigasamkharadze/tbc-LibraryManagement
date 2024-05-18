from django.contrib import admin
from users.models import User, Librarian, Borrower


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'personal_number', 'birth_date', 'is_active', 'is_staff', 'profile')
    list_filter = ('is_active', 'is_staff', 'profile')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'description')
    list_filter = ('position',)


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('user', )
