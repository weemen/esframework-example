from django.conf import settings
from django.core.management.base import BaseCommand
from esframework.data_sources.sqlalchemy.models import SqlDomainRecord

from api.projections.game_state_model import GameStateModel


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        self.stdout.write("Creating esframework default tables:")
        try:
            model = SqlDomainRecord()
            model.metadata.create_all(settings.DB_ENGINE)
            model = GameStateModel()
            model.metadata.create_all(settings.DB_ENGINE)
            self.stdout.write(self.style.SUCCESS("Tables succesfully created"))
        except Exception as ex:
            self.stdout.write(self.style.ERROR("Failed to create tables: {}".format(str(ex))))
