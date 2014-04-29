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
             ],
            name="search_index_recipe",
            weights={
                'title':100,
                'description':25
            }
        )

        db.eathub.webapp_profile.ensure_index(
            [
                ('display_name', 'text'),
                ('location', 'text'),
            ],
            name="search_index_profile",
            weights={
                'display_name':100,
                'location':25
            }
        )

        self.stdout.write('yeah nigga, ya es fuckerday motherfraideis!')

