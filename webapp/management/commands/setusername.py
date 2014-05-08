from pymongo import *
from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand, CommandError
from webapp.models import Profile


class Command(NoArgsCommand):
    help = 'Set the username from User to Profile'

    def handle(self, **options):
        usuarios = User.objects.all()
        self.stdout.write('There are "%s" users' % usuarios.__len__())
        for u in usuarios:
            p = u.profile.get()
            #self.stdout.write('The username is "%s"' % u.username)
            p.username=u.username
            self.stdout.write('The username is "%s"' % p.username)
            p.save()

        self.stdout.write('Done!')

