import time

from django.core.management.base import BaseCommand
from medicines.scheduler import start


class Command(BaseCommand):
    help = "Run the MediSync medicine reminder scheduler"

    def handle(self, *args, **options):
        scheduler = start()

        self.stdout.write(
            self.style.SUCCESS("MediSync reminder scheduler is running.")
        )

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write("MediSync scheduler stopped.")