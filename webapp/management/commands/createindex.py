from pymongo import *
from django.core.management.base import NoArgsCommand, CommandError

class Command(NoArgsCommand):
    help = 'Create index'

    def handle(self, **options):
        db = MongoClient()

        db.eathub.webapp_recipe.ensure_index([("$**", 'text',)], name="recipe_text", default_language = "spanish")
        db.eathub.webapp_profile.ensure_index([("$**", 'text',)], name="profile_text", default_language = "spanish")

        self.stdout.write('Indices creados')

