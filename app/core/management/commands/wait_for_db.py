import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        waitingTime = 1
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                msg = 'Database unavailable, waiting {0} second...'
                msg = msg.format(waitingTime)
                self.stdout.write(msg)
                time.sleep(waitingTime)
                if waitingTime < 60:
                    waitingTime *= 2

        self.stdout.write(self.style.SUCCESS('Database available!'))
