from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation
from reservations.choices import StatusChoices


class Command(BaseCommand):
    help = 'Update reservations status'

    def handle(self, *args, **kwargs):
        one_day_ago = timezone.now() - timedelta(days=1)
        (Reservation.objects
         .filter(date__lte=one_day_ago, status=StatusChoices.ACTIVE)
         .update(status=StatusChoices.INACTIVE)
         )
        self.stdout.write(self.style.SUCCESS('Reservations status updated'))
