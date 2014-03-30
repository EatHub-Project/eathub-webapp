# coding=utf-8

from django.contrib.auth.models import User
from webapp.models import Tastes, Profile
from webapp.models import Author, Recipe, Time, Picture, Savour
from django.test import TestCase
from datetime import datetime

"""
    Para ejecutar las pruebas hay que proceder de la siguiente forma: debemos descomentar la prueba que queramos
    ejecutar ya que, tal y como estan implementadas, si se eleva algun ValidatorError no se ejecutara el siguiente
    test.
"""


class ProfileTest(TestCase):

    def setUp(self):
        pass

    def test_profile_well_created(self):
        pass

class RecipesTestCase(TestCase):

    def setUp(self):
        pass


