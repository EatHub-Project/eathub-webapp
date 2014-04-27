from pymongo import *
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Create index'

    def handle(self, **options):
        db = MongoClient()

        db.eathub.webapp_recipe.ensure_index(
            [
                 ('title', 'text'),
                 ('description', 'text'),
             ]
        )

        db.eathub.webapp_profile.ensure_index(
            [
                ('display_name', 'text'),
                ('location', 'text'),
            ]
        )

        self.stdout.write('yeah nigga, ya es fuckerday motherfraideis!')

