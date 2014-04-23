# coding=utf-8
from django.contrib.auth.management import get_default_username

from django.contrib.auth.models import User
from webapp.models import Tastes, Profile
from webapp.models import Author, Recipe, Time, Picture, Savour, Following
from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError

"""
    Para ejecutar las pruebas hay que proceder de la siguiente forma: debemos descomentar la prueba que queramos
    ejecutar ya que, tal y como estan implementadas, si se eleva algun ValidatorError no se ejecutara el siguiente
    test.
"""


class ProfileTest(TestCase):

    def setUp(self):
        pass

    #tests negativos

    def test_profile_unknown_gender(self):
        md = datetime(2014, 4, 10)
        bd = datetime(1992, 12, 13)
        t = Tastes(salty=1, sour=10, bitter=25, sweet=50, spicy=0)
        u = User.objects.create_user("ricky", "ricky@ricky.com", "rickytaun")
        try:
            p = Profile(display_name="ricky", modification_date=md, main_language="Spanish", additional_languages=[],
                    website="http://juanmanuellopezpazos.appspot.com", gender="Q", birth_date=bd,
                    location="Seville", tastes=t, user=u, following=[])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass


class RecipesNegativeTestCase(TestCase):

    def setUp(self):
        pass
    """
    def test_recipe_main_picture_null(self):
        a = Author()
        s = Savour()
        t = Time(prep_time=20, cook_time=10)
        p = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=None, step=1)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p])
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
    """

    def test_recipe_any_savour_out_of_range(self):
        a = Author()
        s = Savour(salty=500, sour=10, bitter=10, sweet=20, spicy=15)
        t = Time(prep_time=20, cook_time=10)
        p = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=None, step=1)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p])
        try:
            r.clean_fields()
            r.savours.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_recipe_picture_with_invalid_url(self):
        a = Author()
        s = Savour(salty=50, sour=10, bitter=10, sweet=20, spicy=15)
        t = Time(prep_time=20, cook_time=10)
        p = Picture(url="juanmanuellopezpazos.appspot.com/photo.jpg", is_main=True, step=1)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p])
        try:
            r.clean_fields()
            for a in r.pictures:
                a.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
    """
    def test_recipe_main_picture_null(self):
        a = Author()
        s = Savour(salty=50, sour=10, bitter=10, sweet=20, spicy=15)
        t = Time(prep_time=20, cook_time=10)
        p = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=None, step=1)
        print "Valor de is_main: " + str(p.is_main)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p])
        try:
            r.clean_fields()
            for a in r.pictures:
                print "valor de is_main en el for: " + str(a.is_main)
                a.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            print v
    """

    def test_recipe_more_than_one_main_picture(self):
        a = Author()
        s = Savour(salty=50, sour=10, bitter=10, sweet=20, spicy=15)
        t = Time(prep_time=20, cook_time=10)
        p1 = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=True, step=1)
        p2 = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=True, step=2)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p1, p2])
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_recipe_procedure_with_empty_step(self):
        a = Author()
        s = Savour(salty=50, sour=10, bitter=10, sweet=20, spicy=15)
        t = Time(prep_time=20, cook_time=10)
        p1 = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=True, step=1)
        p2 = Picture(url="http://juanmanuellopezpazos.appspot.com/photo.jpg", is_main=None, step=2)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["", " "], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p1, p2])
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            print v

class ProfileNegativeTestCase(TestCase):

    def setUp(self):
        pass

    def test_profile_any_savour_out_of_range(self):
        md = datetime(2014, 4, 10)
        bd = datetime(1992, 12, 13)
        t = Tastes(salty=150, sour=10, bitter=25, sweet=50, spicy=0)
        u = User.objects.create_user("ricky", "ricky@gmail.com", "rickytaun")
        try:
            p = Profile(display_name="ricky", modification_date=md, main_language="Spanish", additional_languages=[],
                    website="http://juanmanuellopezpazos.appspot.com", gender="m", birth_date=bd,
                    location="Seville", tastes=t, user=u, following=[], avatar="images/image.jpg")
            p.clean_fields()
            p.tastes.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass


