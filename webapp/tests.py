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
        except ValidationError as v:
            if v.message_dict.get('gender') is not None:
                print "\n==>Ha intentado introducir un perfil con un genero desconocido.\n"


class RecipesTestCase(TestCase):

    def setUp(self):
        pass

    def test_recipe_difficult_higher_than_3(self):
        a = Author()
        s = Savour()
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=500,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=20)
        try:
            r.clean_fields()
            r.save()
        except ValidationError as v:
            if v.message_dict.get('difficult') is not None:
                print "==>La dificultad debe estar comprendida entre 1 y 3.\n"



