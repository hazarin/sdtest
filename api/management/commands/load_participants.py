from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, transaction
from api import models
import jsonlines


class Command(BaseCommand):
    """
    Загрузка списка участников из participants.jsonl
    """
    help = 'Load participants'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        reader = jsonlines.open(options['file'])
        try:
            with transaction.atomic():
                key = 0
                for obj in reader:
                    key += 1
                    participant = models.Participant.objects.create(name=obj['name'])
                    if key % 100 == 0:
                        self.stdout.write(self.style.SUCCESS(key))
                    for name, value in obj['precedents'].items():
                        try:
                            precedent_catalog = models.PrecedentCatalog.objects.get(name=name)
                        except models.PrecedentCatalog.DoesNotExist as e:
                            precedent_catalog = models.PrecedentCatalog.objects.create(name=name)
                        attitude = 0 if value['attitude'] == 'negative' else 1
                        precedent = models.Precedent.objects.create(precedent=precedent_catalog, attitude=attitude,
                                                     importance=value['importance'], participant=participant)
            self.stdout.write(self.style.SUCCESS('Data loaded'))
        except DatabaseError:
            raise CommandError('Database error')
