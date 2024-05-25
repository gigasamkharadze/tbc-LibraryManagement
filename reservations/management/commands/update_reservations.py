from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation
from reservations.choices import StatusChoices
from django.db.models import F


class Command(BaseCommand):
    help = 'Update reservations status'

    def handle(self, *args, **kwargs):
        one_day_ago = timezone.now() - timedelta(days=1)
        reservations_to_update = Reservation.objects.filter(date__lte=one_day_ago, status=StatusChoices.ACTIVE)

        for reservation in reservations_to_update:
            reservation.book.quantity = F('quantity') + 1
            reservation.book.save()

        reservations_to_update.update(status=StatusChoices.INACTIVE)

        self.stdout.write(self.style.SUCCESS('Reservations status updated and book quantities increased'))
