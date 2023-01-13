import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('../../data/tags.csv') as file:
            reader = csv.reader(file)
            Tag.objects.bulk_create(
                Tag(
                    name=row[0], color=row[1], slug=row[2]
                    ) for row in reader
            )
