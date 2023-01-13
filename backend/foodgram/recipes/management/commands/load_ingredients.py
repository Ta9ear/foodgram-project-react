import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('../../data/ingredients.csv') as file:
            reader = csv.reader(file)
            Ingredient.objects.bulk_create(
                Ingredient(
                    name=row[0], measurement_unit=row[1]
                ) for row in reader
            )
