from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class QuantityFilter(admin.SimpleListFilter):
    title = _('quantity')
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return [
            ('lte5', _('Less than or equal to 5')),
            ('between5and20', _('Between 5 and 20')),
            ('gt20', _('Greater than 20')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'lte5':
            return queryset.filter(quantity__lte=5)
        if self.value() == 'between5and20':
            return queryset.filter(quantity__gt=5, quantity__lte=20)
        if self.value() == 'gt20':
            return queryset.filter(quantity__gt=20)
