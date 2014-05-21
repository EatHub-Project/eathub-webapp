import os
from pymongo import *
from urlparse import urlparse
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Create index'

    def handle(self, **options):
        MONGO_URL = os.environ.get('MONGOHQ_URL')

        if MONGO_URL:
            # Get a connection
            conn = pymongo.Connection(MONGO_URL)

            # Get the database
            db = conn[urlparse(MONGO_URL).path[1:]]
        else:
            # Not on an app with the MongoHQ add-on, do some localhost action
            db = MongoClient()

        db.eathub.webapp_recipe.ensure_index([("$**", 'text',)], name="recipe_text", default_language = "spanish")
        db.eathub.webapp_profile.ensure_index([("$**", 'text',)], name="profile_text", default_language = "spanish")

        self.stdout.write('Indices creados')

