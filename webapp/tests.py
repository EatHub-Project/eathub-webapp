# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from webapp.models import Location, Tastes, Profile, Gender
from django.core.exceptions import ValidationError
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
        gen = Gender(male=1, female=0, other=0)
        p = Profile(main_language="Spanish", website="sloydev.com", gender=gen, location=loc, tastes=t, user=u,
                    modification_date=datetime(2012, 10, 10))

        # Guarda SÓLO la entidad profile, que es la que debe ir en la colección de la bbdd. El resto son entidades embebidas.
        p.save()

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
        self.assertIs(p.gender.male == 1 or p.gender.female == 1 or p.gender.other == 1, True,
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

    def languages_list(self): # Metodo usado en pruebas 31 y 32
        l = list()
        l.append('Spanish')
        l.append('English')
        l.append('French')
        return l

    """
    def validate_country(self, country):  # Prueba numero 28
        if country is None:
            raise ValidationError(u'Country field cannot be empty')
        if self.countries_list.count(country) == 0:
            raise ValidationError(u'%s is not in countries list' % country)

    def validate_city(self, city):  # Prueba numero 29
        if city is not None:
            if city == '':
                raise ValidationError(u'if city is set it cannot be empty')


    def validate_main_language(self, main_language):  # Prueba numero 31
        if main_language is None:
            raise ValidationError(u'Main language cannot be empty')
        else:
            if self.languages_list().count(main_language) == 0:
                raise ValidationError(u'%s is not in languages list' % main_language)

    def validate_additional_languages(self, additional_languages):  # Prueba numero 32
        if additional_languages is not None:
            for a in additional_languages:
                if self.languages_list().count(a) == 0:
                    raise ValidationError(u'%s is not in languages list' % additional_languages)

    def validate_gender(self, gender):  # Prueba numero 35
        if not (gender.male == 1 or gender.female == 1 or gender.other == 1):
            raise ValidationError(u'%s is not a valid gender' % gender)


    def validate_modification_date(self, modification_date):  # Prueba numero 37
        if type(modification_date) is not date:  # si no funciona probar con datetime
            raise ValidationError(u'%s is not a date object' % modification_date)

    def validate_first_name(self, first_name):  # Prueba numero 39
        if first_name is None:
            raise ValidationError(u'the first name cannot be None')

    def validate_password(self, password): # Prueba numero 40
        if password.length < 8:
            raise ValidationError(u'the password must be at least 8 characters')

    def validate_email(self, email): # Prueba numero 41
        if len(email) > 50 or email is None:
            raise ValidationError(u'Email must be at most 50 characters')

    def validate_last_login(self, last_login):  # Prueba numero 43
        if type(last_login) is not datetime:
            raise ValidationError(u'last login type must be date')
        if last_login is None:
            raise ValidationError(u'last login cannot be None')
        fecha = datetime.today()
        if last_login > fecha:
            raise ValidationError(u'last_login date cannot be after current date')"""




