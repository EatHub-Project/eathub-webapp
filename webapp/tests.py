# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from webapp.models import Location, Tastes, Profile


class ProfileTest(TestCase):
    def setUp(self):
        # Crea un usuario normal
        # Como se usa el método create_user(), automáticamente se guarda en la BBDD.
        u = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        # Crea las entidades
        loc = Location(country="Spain", city="Huerba")
        t = Tastes(salty="5", sour="6", bitter="7", sweet="8", spicy="8")
        p = Profile(main_language="Spanish", website="sloydev.com", sex="male", location=loc, tastes=t, user=u)

        # Guarda SÓLO la entidad profile, que es la que debe ir en la colección de la bbdd. El resto son entidades embebidas.
        p.save()

    def test_recipe_well_created(self):
        # Prueba MUY básica para obtener el objeto y mostrar algunos campos. Se deberían hacer otro tipo de pruebas unitarias
        p = Profile.objects.get()
        self.assertEqual(p.user.username, "john")
        print str(p)
        print str(p.location)
        print str(p.user)
        print str(p.user.email)