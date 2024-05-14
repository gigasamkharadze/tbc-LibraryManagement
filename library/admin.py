from django.contrib import admin
from django.db.models import Count

from library.models import Book, Author, Genre
from library.filters import QuantityFilter


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    list_filter = ('date_of_birth', 'date_of_death')
    ordering = ('last_name', 'first_name', 'date_of_birth')


from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'publication_date', 'quantity', 'total_borrowed',
                    'reservations_count', 'currently_borrowed')
    search_fields = ('title', 'author__first_name', 'author__last_name', 'genre__name', 'publication_date', 'quantity')
    list_filter = ('genre', 'publication_date')
    ordering = ('title', 'publication_date', 'author', 'quantity')
    list_per_page = 100

    def get_queryset(self, request):
        return (super().get_queryset(request)
                .select_related('author')
                .prefetch_related('genre', 'transactions', 'reservations'))

    def display_genre(self, book):
        return ", ".join([genre.name for genre in book.genre.all()])
    display_genre.short_description = 'Genre'

    def total_borrowed(self, book):
        return book.transactions.count()
    total_borrowed.short_description = 'Total Borrowed'

    def reservations_count(self, book):
        return book.reservations.count()
    reservations_count.short_description = 'Reserved'

    def currently_borrowed(self, book):
        return book.transactions.filter(return_date__isnull=True).count()
    currently_borrowed.short_description = 'Currently Borrowed'
