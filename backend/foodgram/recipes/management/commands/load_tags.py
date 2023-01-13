import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")

    def handle(self, *args, **options):
        file_path = options["path"]

        with open(file_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            Tag.objects.bulk_create(
                Tag(
                    name=row[0], color=row[1], slug=row[2]
                ) for row in reader
            )
