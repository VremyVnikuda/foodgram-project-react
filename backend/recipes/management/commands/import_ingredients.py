import csv

from django.core.management.base import BaseCommand
from foodgram_backend.settings import CSV_DIR
from recipes.models import Ingredient


def import_data():
    """Чтение файла CSV/создания экземпляров модели"""
    with open(
        f'{CSV_DIR}/ingredients.csv',
        encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Ingredient.objects.create(
                name=row['название'],
                measurement_unit=row['единица измерения'],
            )


class Command(BaseCommand):
    help = 'Импорт ингридиентов'

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(
            self.style.SUCCESS('Ингридиенты загружены в базу')
        )
