# coding=utf-8

from django.contrib.auth.models import User
from webapp.models import Recipe, Time, Step
from django.test import TestCase
from datetime import datetime
from webapp.models import Tastes, Profile, Following, Savour
from django.core.exceptions import ValidationError

"""
    Para ejecutar las pruebas hay que proceder de la siguiente forma: debemos descomentar la prueba que queramos
    ejecutar ya que, tal y como estan implementadas, si se eleva algun ValidatorError no se ejecutara el siguiente
    test.
"""


class RecipeTest(TestCase):
    def setUp(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[picture], main_image=picture)
        r.save()

    def test_recipe_title(self):
        r = Recipe.objects.filter(title="receta de prueba")[0]
        self.assertNotEquals(r.title, "Loren Ipsum")



"""
class RecipesNegativeTestCase(TestCase):

    def setUp(self):
        pass

    def test_recipe_difficult_higher_than_3(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=500,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de dificultad.\n")
        except ValidationError as v:
            pass

    def test_recipe_cook_time_less_than_zero(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = -10)
        step = Step(text="Step", image=None)
        #picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de cook time < 0.\n")
        except ValidationError as v:
            pass

    def test_recipe_preparation_time_and_cook_time_none(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = None, cook_time = None)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de dificultad.\n")
        except ValidationError as v:
            pass


    def test_recipe_preparation_time_less_than_zero(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = -1, cook_time = None)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de prep time < 0.\n")
        except ValidationError as v:
            pass


    def test_recipe_steps_not_none(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step, None], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_recipe_steps_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de steps not blank.\n")
        except ValidationError as v:
            pass


    def test_recipe_serves_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_recipe_title_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_recipe_description_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_special_conditions_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
    #        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[""],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass



    def test_temporality_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=[""], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_nationality_not_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_recipe_no_more_ten_tags(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1","Tag 1","Tag 1","Tag 1","Tag 1","Tag 1","Tag 1","Tag 1","Tag 1","Tag 1","Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass

    # Comprobar si ha cambiado
    def test_food_type_association(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
#        picture = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        auxiliar_recipe = Recipe.objects.filter(title="Carne con tomate")
        picture = auxiliar_recipe.pictures[0]
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="", time=time_recipe, pictures = [picture], main_image = picture)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass


    def test_pictures_association(self):
        a = User()
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = -10)
        picture = Picture(url = "http://www.sevibus.com", is_main = True, step = 1)
        r = Recipe(title="", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language="Spanish", temporality=["Spring"], nationality="", difficult=500,
                   steps=("Step 1", "Step 2"), author=a, tags=["Tag 1", "Tag 2"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures= [])
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_recipe_ingredients_list_not_blank(self):
        a = User()
        s = Savour()
        time_recipe = Time(prep_time = 5, cook_time = 10)
        picture = Picture(url = "http://www.sevibus.com", is_main = True, step = 1)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=(),
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture])
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    def test_recipe_ingredients_list_not_none_item(self):
        a = User()
        s = Savour()
        time_recipe = Time(prep_time = 5, cook_time = 10)
        picture = Picture(url = "http://www.sevibus.com", is_main = True, step = 1)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=("Oil", None),
                   serves="2", language="Spanish", temporality="Spring", nationality="Spain", difficult=2,
                   steps=["Paso 1", "Paso 2"], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures = [picture])
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass
"""
