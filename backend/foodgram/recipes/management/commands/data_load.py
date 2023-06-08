from csv import DictReader

from django.core.management import BaseCommand, CommandError
from recipes.models import Ingredient

TABLES_DICT = {
    Ingredient: ('ingredients.csv', ['name', 'measurement_unit']),
}


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **options):
        for model, parameters in TABLES_DICT.items():
            if model.objects.exists():
                raise CommandError('Data exists in database!')
            with open(
                    f'./{parameters[0]}',
                    encoding='utf-8'
            ) as csv_file:
                reader = DictReader(csv_file)
                data = []
                for row in reader:
                    data.append(model(
                        **dict(zip(parameters[1], row.values()))
                    ))
                model.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS('Successfully load data'))
