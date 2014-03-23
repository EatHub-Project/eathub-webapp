# coding=utf-8

from django.test import TestCase
from webapp.models import Author, Recipe, Time, Picture


class RecipesTestCase(TestCase):
    def setUp(self):
        # Aquí se prepara la base de datos con los datos de prueba.

        # Las entidades embebidas se pueden crear antes, o directamente cuando se crea la receta
        a = Author(displayName="Rafa Vázquez", userName="sloydev")
        r = Recipe(title="Cosas ricas de prueba",
                   description="Una receta muy rica para probar que el modelo funciona correctamente en la base de datos y tal.",
                   steps=["Paso uno", "Paso dos", "Paso tres"],
                   serves="Siete personas",
                   language="spanish",
                   temporality=["christmas", "summer"],
                   pictures=[Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08368-1600x1200.jpg",
                                     step=1),
                             Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08371-1600x1200.jpg",
                                     step=2),
                             Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08380-1600x1200.jpg",
                                     isMain=True)],
                   time=Time(prepTime=20, cookTime=0),
                   author=a)
        r.save()

    def test_recipe_well_created(self):
        # Prueba MUY básica para obtener el objeto y mostrar algunos campos. Se deberían hacer otro tipo de pruebas unitarias
        r = Recipe.objects.get()
        self.assertEqual(r.title, "Cosas ricas de prueba")
        print str(r)
        print str(r.pictures)
        print str(r.time)
