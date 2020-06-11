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
                for key, obj in enumerate(reader):
                    participant = models.Participant.objects.create(name=obj['name'])
                    if key % 100 == 0:
                        self.stdout.write(self.style.SUCCESS(str(key)))
                    for name, value in obj['precedents'].items():
                        precedent_catalog = models.PrecedentCatalog.objects.get_or_create(name=name)
                        importance = -value['importance'] if value['attitude'] == 'negative' else value['importance']
                        models.Precedent.objects.create(
                            precedent=precedent_catalog[0],
                            importance=importance,
                            participant=participant
                        )
            self.stdout.write(self.style.SUCCESS('Data loaded'))
        except DatabaseError:
            raise CommandError('Database error')
