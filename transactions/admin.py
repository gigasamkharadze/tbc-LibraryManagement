from django.contrib import admin
from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'checkout_date', 'return_date')
    search_fields = ('book__title', 'checkout_date', 'return_date')
    list_filter = ('borrower', 'checkout_date', 'return_date', 'book')
