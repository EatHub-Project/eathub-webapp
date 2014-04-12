from django.core.management.base import NoArgsCommand, CommandError
from webapp.models import User, Recipe, Vote, Author, Profile
from bson import ObjectId

class Command(NoArgsCommand):
    help = 'Calculate de karma for all users'

    def handle(self, **options):
        usuarios = User.objects.all()
        self.stdout.write('There are "%s" users' % usuarios.__len__())
        for u in usuarios:
            p = u.profile.get()
            recipes = list(Recipe.objects.raw_query({'author.user_id': ObjectId(u.id)}))
            pos = 0
            neg = 0
            for r in recipes:
                pos+= r.positives.__len__()
                neg+= r.negatives.__len__()
            p.karma = 6 + (recipes.__len__()*0.2)+(pos*0.1)-(neg*0.1)
            p.save()
            self.stdout.write('The user "%s"' % u.username)
            self.stdout.write('have karma "%s"' % p.karma)

        self.stdout.write('Successfully calculate karma')