import os
from django.apps import AppConfig


class RatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rates"
    path = os.path.dirname(os.path.abspath(__file__))
    verbose_name = "Parking Rates"

    # Keeping this to show of a failed attempt to seed db on start
    # Received 'AppRegistryNotReady("Apps aren't loaded yet.")' error.

    # def ready(self):
    #     """Overriding 'ready' method to perform initialization tasks"""


    # Could have possbily tried calling ready first: super().ready()
    # Then running seeding function that is located inside this class

#     if apps.ready:
#         print("Seeding database...")
#         seed_database_with_parking_rates()
#         print("Success!")
#     else:
#         print("Rates app is not ready - seeding database failed :(")
