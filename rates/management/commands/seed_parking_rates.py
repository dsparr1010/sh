from django.core.management.base import BaseCommand
from rates.seed import seed_database_with_parking_rates


class Command(BaseCommand):
    help = "Seeds the databse with a json file of parking rates"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        seed_database_with_parking_rates()
        self.stdout.write("Success!")
