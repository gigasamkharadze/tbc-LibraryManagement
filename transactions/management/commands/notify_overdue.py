from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from transactions.models import Transaction
from django.conf import settings
from django.utils import timezone
import logging


class Command(BaseCommand):
    help = 'Sends an email to borrowers with overdue books'

    def handle(self, *args, **options):
        overdue_transactions = \
            (Transaction.objects
             .filter(return_date__isnull=True)
             .filter(due_date__lt=timezone.now().date())
             .select_related('borrower__user')
             .all())

        messages = []
        for transaction in overdue_transactions:
            message = (
                'Overdue book return',
                f'You have an overdue book: {transaction.book}. Please return it as soon as possible.',
                settings.EMAIL_HOST_USER,
                [transaction.borrower.user.email],
            )
            messages.append(message)

        try:
            send_mass_mail(messages, fail_silently=False)
            self.stdout.write(self.style.SUCCESS('Successfully sent emails to borrowers with overdue books'))
        except Exception as e:
            logging.error(f"Failed to send emails: {e}")
