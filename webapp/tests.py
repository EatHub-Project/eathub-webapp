# coding=utf-8

from django.contrib.auth.models import User
from webapp.models import Location, Tastes, Profile
from webapp.models import Author, Recipe, Time, Picture, Savour
from django.test import TestCase
from datetime import datetime


class ProfileTest(TestCase):
    def setUp(self):
        # Crea un usuario normal
        # Como se usa el método create_user(), automáticamente se guarda en la BBDD.
        last_login = datetime(2010, 10, 10)
        u = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        # Crea las entidades
        loc = Location(country="Spain", city="Huerba")
        t = Tastes(salty="5", sour="6", bitter="7", sweet="8", spicy="8")
        # Guarda SÓLO la entidad profile, que es la que debe ir en la colección de la bbdd. El resto son entidades embebidas.
        Profile.objects.create(main_language="Spanish", additional_languages=["English"], website="sloydev.com",
                               gender="m", location=loc, tastes=t, user=u, modification_date=datetime(2012, 10, 10))

    def test_recipe_well_created(self):
        # Prueba MUY básica para obtener el objeto y mostrar algunos campos. Se deberían hacer otro tipo de pruebas unitarias
        p = Profile.objects.get()
        self.assertEqual(p.user.username, "john")

        # Prueba numero 28
        self.assertIsNotNone(p.location.country, "The country cannot be None.")
        self.assertIn(p.location.country, self.countries_list(), "The country must be in countries list.")
        # Prueba numero 29
        self.assertIsNot(p.location.city is not None, p.location.city == '', "The city cannot be empty if it's set.")
        #Prueba numero 31
        self.assertIsNotNone(p.main_language, "The main language cannot be None.")
        self.assertIn(p.main_language, self.languages_list(), "The main language is not in languages list.")
        #Prueba 32
        for a in p.additional_languages:
            self.assertIn(a, self.languages_list(), "There is an additional language not "
                                                    "avaible in additional languages.")

        # Prueba numero 35
        self.assertIs(p.gender == "u" or p.gender == "m" or p.gender == "f", True,
                      "The gender must be specified.")

        # Prueba numero 37
        self.assertIs(type(p.modification_date) == datetime, True, "The modification date is not a valid date object.")
        #Prueba numero 39
        self.assertIsNotNone(p.user.first_name, "The first name user cannot be None.")
        # Prueba numero 40
        self.assertIs(len(p.user.password) >= 8, True, "The password must be 8 characters at least.")
        # Prueba numero 41
        self.assertIs(len(p.user.email) <= 50, p.user.email is not None, "Email must be 50 characters at most.")
        # Prueba numero 43

        print "Fecha ultimo login: " + str(p.user.last_login)
        print "Fecha actual: " + str(datetime.today())
        print "Tipo de la ultima fecha de login: " + str(type(p.user.last_login))
        self.assertIs(type(p.user.last_login) == datetime, p.user.last_login is not None,
                      "Date must be set and must be a date object")

        self.assertIs(datetime.today().day >= p.user.last_login.day, True, "Last login date cannot be after today")
        self.assertIs(datetime.today().month >= p.user.last_login.month, True, "Last login date cannot be after today")
        self.assertIs(datetime.today().year >= p.user.last_login.year, True, "Last login date cannot be after today")

        print str(p)
        print str(p.location)
        print "User: " + str(p.user)
        print "Email: " + str(p.user.email)

    def countries_list(self):  # Metodo usado en la prueba numero 28
        l = list()
        l.append('Spain')
        l.append('England')
        l.append('France')
        l.append('Germany')
        return l

    def languages_list(self):  # Metodo usado en pruebas 31 y 32
        l = list()
        l.append('Spanish')
        l.append('English')
        l.append('French')
        return l


class RecipesTestCase(TestCase):
    def setUp(self):
        # Aquí se prepara la base de datos con los datos de prueba.

        # Las entidades embebidas se pueden crear antes, o directamente cuando se crea la receta
        u = User.objects.create_user('bruce', 'bruce@harddie.com', 'brucepassword')
        loc = Location(country="Spain", city="Huerba")
        t = Tastes(salty="5", sour="6", bitter="7", sweet="8", spicy="8")
        p = Profile(main_language="Spanish", additional_languages=["English"], website="sloydev.com", gender="m", location=loc, tastes=t, user=u,
                    modification_date=datetime(2012, 10, 10))

        a = Author(display_name="Rafa Vázquez", user_name="sloydev", user=p)
        s = Savour(salty=10, sour=1, bitter=1, sweet=1, spicy=1)
        Recipe.objects.create(title="Cosas ricas de prueba",
                   description="Una receta muy rica para probar que el modelo funciona correctamente en la base de datos y tal.",
                   steps=["Paso uno", "Paso dos", "Paso tres"],
                   serves="Siete personas",
                   language="spanish",
                   creation_date='2014-03-24',
                   modification_date=None,
                   is_published=True,
                   parent=None,
                   temporality=["christmas", "summer"],
                   nationality='spain',
                   special_conditions=["glutenfree"],
                   notes="ola k ase",
                   difficult=3,
                   food_type="cangrejo a la carbonara",
                   tags=["glutenfree", "summer", "christmas", "spain", "ricas", "cosas", "prueba", "asd", "asdfa", "asdasdf", "ñklja"],
                   pictures=[Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08368-1600x1200.jpg",
                                     step=1),
                             Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08371-1600x1200.jpg",
                                     step=2),
                             Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08380-1600x1200.jpg",
                                     is_main=True)],
                   time=Time(prep_time=20, cook_time=0),
                   ingredients=["lo que sea"],
                   savours=s,
                   author=a)
        #r.clean_fields()

    def test_recipe_well_created(self):
        # Prueba MUY básica para obtener el objeto y mostrar algunos campos. Se deberían hacer otro tipo de pruebas unitarias
        r = Recipe.objects.get()
        self.assertEqual(r.title, "Cosas ricas de prueba")
        print str(r)
        print str(r.pictures)
        print str(r.time)
        print str(r.creation_date)
        print str(r.is_published)
        #Falta probar el atributo reflexivo
        print str(r.nationality)
        print str(r.special_conditions)
        print str(r.notes)
        print str(r.difficult)
        print str(r.food_type)
        print str(r.tags)
        print str(r.ingredients)
        print str(r.savours)
        savours_test = Recipe.objects.get(title="Cosas ricas de prueba").savours
        #self.assertIs(savours_test.salty <= -1 or savours_test.salty >= 100, True, "Savour value is not in range 0, 99")
        #self.assertIs(savours_test.sour <= -1 or savours_test.sour >= 100, True, "Savour value is not in range 0, 99")
        #self.assertIs(savours_test.bitter <= -1 or savours_test.bitter >= 100, True, "Savour value is not in range 0, 99")
        #self.assertIs(savours_test.sweet <= -1 or savours_test.sweet >= 100, True, "Savour value is not in range 0, 99")
        #self.assertIs(savours_test.spicy <= -1 or savours_test.spicy >= 100, True, "Savour value is not in range 0, 99")
