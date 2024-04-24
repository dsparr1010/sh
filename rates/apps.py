import os
from django.apps import AppConfig, apps
from rates.seed import seed_database_with_parking_rates


class RatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rates"
    path = os.path.dirname(os.path.abspath(__file__))
    verbose_name = "Parking Rates"
    # default = True

    def ready(self):
        """Overriding 'ready' method to perform initialization tasks"""
        if apps.ready:
            # print("Seeding database...")
            seed_database_with_parking_rates()
            # print("Success!")
        else:
            print("Rates app is not ready - seeding database failed :(")
