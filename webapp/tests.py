# coding=utf-8

from django.test import TestCase
from webapp.models import Author, Recipe, Time, Picture, Savour


class RecipesTestCase(TestCase):
    def setUp(self):
        # Aquí se prepara la base de datos con los datos de prueba.

        # Las entidades embebidas se pueden crear antes, o directamente cuando se crea la receta
        a = Author(displayName="Rafa Vázquez", userName="sloydev")
        s = Savour(salty = -1, sour = 1, bitter = 1, sweet = 1, spicy = 1)
        r = Recipe(title="Cosas ricas de prueba",
                   description="Una receta muy rica para probar que el modelo funciona correctamente en la base de datos y tal.",
                   steps=["Paso uno", "Paso dos", "Paso tres"],
                   serves="Siete personas",
                   language="spanish",
				   creationDate='2014-03-24',
				   isPublished=True,
				   parent=None,
                   temporality=["christmas", "summer"],
				   nationality='spain',
				   specialConditions=["glutenfree"],
				   notes="ola k ase",
				   difficult=4,
				   foodType="cangrejo a la carbonara",
				   tags=["glutenfree", "summer", "christmas", "spain", "ricas", "cosas", "prueba"],
                   pictures=[Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08368-1600x1200.jpg",
                                     step=1),
                             Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08371-1600x1200.jpg",
                                     step=2),
                             Picture(url="http://www.cocinillas.es/wp-content/uploads/2011/05/DSC08380-1600x1200.jpg",
                                     isMain=True)],
                   time=Time(prepTime=20, cookTime=0),
				   ingredients="lo que sea",
				   #savours=None,
				   savours=s,
                   author=a)
        r.clean_fields()
        r.save()

    def test_recipe_well_created(self):
        # Prueba MUY básica para obtener el objeto y mostrar algunos campos. Se deberían hacer otro tipo de pruebas unitarias
        r = Recipe.objects.get()
        self.assertEqual(r.title, "Cosas ricas de prueba")
        print str(r)
        print str(r.pictures)
        print str(r.time)
        print str(r.creationDate)
        print str(r.isPublished)
        #Falta probar el atributo reflexivo
        print str(r.nationality)
        print str(r.specialConditions)
        print str(r.notes)
        print str(r.difficult)
        print str(r.foodType)
        print str(r.tags)
        print str(r.ingredients)
        print str(r.savours)