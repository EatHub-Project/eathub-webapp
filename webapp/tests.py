# coding=utf-8

from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError
from webapp.models import Tastes, Profile, Following, Temporality,Food_Type,Special_Condition,Vote

"""
    Para ejecutar las pruebas hay que proceder de la siguiente forma: debemos descomentar la prueba que queramos
    ejecutar ya que, tal y como estan implementadas, si se eleva algun ValidatorError no se ejecutara el siguiente
    test.
"""


class ProfileTest(TestCase):

    def setUp(self):
        pass

    def test_profile_unknown_gender(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u, modification_date = md, gender = "x", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f], karma = 6)
        try:
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_profile_unknown_name(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Sevilla", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_profile_unknown_additional_languages(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=None,
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Seville", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_profile_unknown_additional_language(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=[None],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_profile_unknown_website(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="esto no es una url", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_profile_unknown_location(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.pedro.com", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location=None, tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_profile_unknown_tastes(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=-1, sour=900, bitter=3, sweet=3, spicy=3)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.pedro.com", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            t.clean_fields()
            t.save()
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    """Las pruebas que faltaban comienzan a partir de aqui"""

    def test_profile_invalid_birth_date(self):
        md = datetime(2014, 4, 10)
        b = datetime(2015, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        p = Profile(display_name="juan", main_language="English", website="http://www.jajajaja.com/",
                    tastes=t, user=u, modification_date=md, gender="m",
                    avatar="images/i100236495_91881_5.jpg", birth_date=b, location="Sevilla",
                    additional_languages=[], following=[f], karma=6)
        try:
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al definirse una fecha de nacimiento invalida.\n")
        except ValidationError as v:
            print v

    def test_profile_invalid_modification_date(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        p = Profile(display_name="juan", main_language="English", website="http://www.jajajaja.com/",
                    tastes=t, user=u, modification_date=md, gender="m",
                    avatar="images/i100236495_91881_5.jpg", birth_date=b, location="Sevilla",
                    additional_languages=[], following=[f], karma=6)
        try:
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al definirse una fecha de modificacion invalida.\n")
        except ValidationError as v:
            pass

    def test_profile_existing_email(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'artjimlop@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        p = Profile(display_name="juan", main_language="English", website="http://www.jajajaja.com/",
                    tastes=t, user=u, modification_date=md, gender="m",
                    avatar="images/i100236495_91881_5.jpg", birth_date=b, location="Sevilla",
                    additional_languages=[], following=[f], karma=6)
        try:
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al especificar un email almacenado en el sistema.\n")
        except ValidationError as v:
            pass
