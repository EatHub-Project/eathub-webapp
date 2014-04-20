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
""" Avatar no tiene restricciones
    def test_profile_unknown_avatar(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="dsffjkl//", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
"""
""" DE DONDE SALE?!
    def test_profile_unknown_username(self):

        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("pedro", "juanmacias@gmail.com", "1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.website.com/", gender="f",avatar="images/i100236495_91881_5.jpg", birth_date=bd, location="Seville", tastes=t, user=u, following=[f])
        try:
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            print v
"""

""" Esto puede ser null asi que no se mira
    def test_profile_unknown_modification_date_(self):
        md = datetime(1900, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

 """

""" no se sabe si tinen restriccion

    def test_profile_unknown_main_language(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="Andaluz", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:

             pass
 """

"""
    def test_profile_unknown_additional_languages(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=["stanilines"],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

 """
"""
    def test_profile_unknown_avatar(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="dsffjkl//", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

 """\
"""
    def test_profile_unknown_website(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.pedro.com", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
 """

"""


    def test_profile_unknown_birth_date(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2011, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.pedro.com", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
 """
"""
 """
"""
    def test_profile_unknown_user_(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=4, sour=3, bitter=3, sweet=3, spicy=3)
        u = User.objects.create_user("lelo", "lelomacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="juan", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.pedro.com", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
 """

"""
    def test_following_well_created(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=4, sour=3, bitter=3, sweet=3, spicy=3)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name ="homie", username = "homie", user = u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.pedro.com", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

 """
"""


class RecipesTestCase(TestCase):

    def setUp(self):

        paux = Profile.objects.filter(display_name="juan")
        paux.delete()
        # Crea un usuario normal
        # Como se usa el método create_user(), automáticamente se guarda en la BBDD.
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', 'testazo1234')

        f = Following(display_name ="homie", username = "homie", user=u)
        t = Savour(salty=None, sour=None, bitter=None, sweet=None, spicy=None)
        # Crea las entidades
        temporality = Temporality("Summer")
        food_type = Food_Type("Comida de ejemplo")
        special_condition = Special_Condition("Condicion")
        t = Tastes(salty=None, sour=None, bitter=None, sweet=None, spicy=None)
        p = Profile(display_name="juan", main_language="English", website="http://www.jajajaja.com/",  tastes=t, user=u,
                    modification_date=None, gender="f", avatar="images/i100236495_91881_5.jpg", birth_date=b,
                    location="Stalingrado", additional_languages=[], following=[f])

        #author = Author(p.display_name, u.username, u)
        author = Author("juan", u.username, u)

        picture = Picture("http://www.sevibus.com", True, 1)
        date_vote_1 = datetime(2010, 10, 10)
        date_vote_2 = datetime(2010, 10, 10)
        vote_positive = Vote(date_vote_1, u)
        vote_negative = Vote(date_vote_2, u)
        time = Time(10, 10)
        r = Recipe(title="titulo de la receta", description="receta" ,creation_date= b, modification_date = None,
                   ingredients=["ingrediente1", "ingrediente2"], temporality=[temporality], nationality="Spanish",
                   notes="nota de ejemplo", difficult=1, food_type="food_type", special_conditions= [special_condition],
                   language="es", serves="1",tags=["Tag 1", "Tag 2"] , steps=["Paso 1", "Paso 2"] , is_published=True,
                   parent= None, author = author, pictures =[picture] , time =time, savours =t ,
                   positives = [vote_positive], negatives = [vote_negative])

        r.save()
"""