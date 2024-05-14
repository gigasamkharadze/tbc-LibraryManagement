from django.contrib import admin
from library.models import Book, Author, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    list_filter = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    ordering = ('last_name', 'first_name', 'date_of_birth')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('author', 'display_genre', 'title', 'publication_date', 'quantity')
    search_fields = ('author', 'title', 'publication_date', 'quantity')
    list_filter = ('author', 'title', 'publication_date', 'quantity')
    ordering = ('title', 'publication_date', 'author', 'quantity')

    def display_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    display_genre.short_description = 'Genre'