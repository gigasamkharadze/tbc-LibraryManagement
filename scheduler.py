from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(call_command, 'interval', hours=1, args=['update_reservations'])
    scheduler.start()
