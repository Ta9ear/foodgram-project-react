import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")

    def handle(self, *args, **options):
        file_path = options["path"]

        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            Ingredient.objects.bulk_create(
                Ingredient(
                    name=row[0], measurement_unit=row[1]
                ) for row in reader
            )
