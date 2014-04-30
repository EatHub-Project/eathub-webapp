# coding=utf-8

from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError
from webapp.models import Language, Recipe, Time, Step, Picture, Savour, Tastes, Profile, Following, \
    Temporality, Food_Type, Special_Condition, Vote

"""
    Para ejecutar las pruebas hay que proceder de la siguiente forma: debemos descomentar la prueba que queramos
    ejecutar ya que, tal y como estan implementadas, si se eleva algun ValidatorError no se ejecutara el siguiente
    test.
"""


class ProfileNegativeTests(TestCase):

    def setUp(self):
        pass

    # Prueba numero 7
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

    # Prueba numero 36
    def test_profile_unknown_gender(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",
                    tastes=t, user=u, modification_date=md, gender="x",
                    avatar="images/i100236495_91881_5.jpg",birth_date=b,location="Sevilla",
                    additional_languages=[], following=[f], karma=6)
        try:
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al definirse un género desconocido.\n")
        except ValidationError as v:
            pass

    # Prueba numero 30
    def test_profile_unknown_display_name(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name="homie", username="homie", user=u)
        try:
            p = Profile(display_name="", modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg",
                    birth_date=bd, location="Sevilla", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al tener display_name vacio..\n")
        except ValidationError as v:
            pass

    # Prueba numero 30
    def test_profile_null_display_name(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name="homie", username="homie", user = u)
        l = Language(code="en")
        try:
            p = Profile(display_name=None, modification_date=md, main_language="English", additional_languages=[],
                    website="http://www.jajajaja.com/", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Sevilla", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    """Esta prueba va a fallar hasta que se solucione el tema del validator"""

    # Prueba numero 35
    def test_profile_invalid_website(self):
        md = datetime(2014, 4, 10)
        bd = datetime(2010, 10, 10)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        u = User.objects.create_user("juan", "juanmacias@gmail.com", "testazo1234")
        f = Following(display_name="homie", username="homie", user=u)
        try:
            p = Profile(display_name="jesus", modification_date=md, main_language="English", additional_languages=[],
                    website="esto no es una url", gender="m",avatar="images/i100236495_91881_5.jpg", birth_date=bd,
                    location="Stalingrado", tastes=t, user=u, following=[f])
            p.clean_fields()
            p.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

class RecipeTest(TestCase):
    def setUp(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        l = "es"
        p = Picture(image="images/i100236495_91881_5.jpg")
        m = "images/i100236495_91881_5.jpg"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        r.save()

    def test_recipe_title(self):
        r = Recipe.objects.filter(title="receta de prueba")[0]
        self.assertNotEquals(r.title, "Loren Ipsum")


class RecipesNegativeTestCase(TestCase):

    def setUp(self):
        pass

    # Prueba numero 23 -- OK
    def test_recipe_difficult_higher_than_3(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        l = "es"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=500,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de dificultad.\n")
        except ValidationError as v:
            pass

    # Prueba numero 11 -- OK
    def test_recipe_cook_time_less_than_zero(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = -10)
        step = Step(text="Step", image=None)
        p = Picture(image = 'http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        l = "es"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de cook time < 0.\n")
        except ValidationError as v:
            pass

    # Prueba numero 12 -- OK
    def test_recipe_preparation_time_and_cook_time_none(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=None, cook_time=None)
        step = Step(text="Step", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        l = "es"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de dificultad.\n")
        except ValidationError as v:
            pass

    # Prueba numero 10 -- OK
    def test_recipe_preparation_time_less_than_zero(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        l = "es"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=-1, cook_time=10)
        step = Step(text="Step", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')

        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.time.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de prep time < 0.\n")
        except ValidationError as v:
            pass

    # Prueba numero 17 -- OK
    def test_recipe_with_none_steps(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        l = "es"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step, None], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            pass

    # Prueba numero 17 -- OK
    def test_recipe_with_blank_steps(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        l = "es"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al haber pasos vacios.\n")
        except ValidationError as v:
            pass

    # Prueba numero 14 -- OK
    def test_recipe_with_none_serves(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        l = "es"
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves=None, language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al ser nulos los comensales.\n")
        except ValidationError as v:
            pass

    # Prueba numero 15 -- OK
    def test_recipe_with_blank_title(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        a = p.user
        s = Savour()
        l = "es"
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al tener el titulo vacio.\n")
        except ValidationError as v:
            pass

    # Prueba numero 16 -- OK
    def test_recipe_with_blank_description(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",
                    tastes=t, user=u,modification_date=md, gender="f", avatar="images/i100236495_91881_5.jpg",
                    birth_date=b, location="Sevilla", additional_languages=[], following=[f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        l = "es"
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="receta de prueba", description="", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de descripcion.\n")
        except ValidationError as v:
            pass

    # Prueba numero 18 -- FAIL
    def test_recipe_with_blank_temporality(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        a = p.user
        s = Savour()
        l = "es"
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
        p = Picture(image="http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg")
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=[], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            print v

    # Prueba numero 18 -- FAIL
    def test_recipe_with_null_temporality(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",
                    tastes=t, user=u, modification_date=md, gender="f", avatar="images/i100236495_91881_5.jpg",
                    birth_date=b,location="Sevilla",additional_languages = [], following=[f])
        p.save()
        a = p.user
        s = Savour()
        l = "es"
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=None, nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de step not None.\n")
        except ValidationError as v:
            print v

    # Prueba numero 19 -- OK
    def test_recipe_with_null_nationality(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan", main_language="English", website="http://www.facebook.com/juanmacias",
                    tastes=t, user=u, modification_date= md, gender="f", avatar="images/i100236495_91881_5.jpg",
                    birth_date=b, location="Sevilla", additional_languages=[], following=[f])
        p.save()
        l = "es"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality=None, difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al haber una nacionalidad nula.\n")
        except ValidationError as v:
            pass

    # Prueba numero 24 -- OK
    def test_recipe_with_more_than_ten_tags(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        l = "es"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1","Tag 2","Tag 3","Tag 4","Tag 5","Tag 6","Tag 7","Tag 8",
                                                 "Tag 9","Tag 10","Tag 11"], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[p], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al haber mas de 10 tags.\n")
        except ValidationError as v:
            pass

    # Prueba numero 25 -- OK
    def test_recipe_with_null_food_type(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)

        # Crea las entidades

        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        l = "es"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
        p = Picture(image='http://2.bp.blogspot.com/-lo44t43gxOw/UO3AhcjhMHI/AAAAAAAAAzI/_Y_DcZowe0k/s1600/albondigas_con_tomate.jpg')
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality=["Spring"], nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=["Tag 1"], notes="Nota", special_conditions=[],
                   savours=s, food_type=None, time=time_recipe, pictures = [p], main_image = m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado en el test de tipo de comida.\n")
        except ValidationError as v:
            pass

    # Prueba numero 13 -- FAIL
    def test_recipe_ingredients_list_blank(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name ="juan", username = "juan", user = u)
        l = "es"
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)

        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        a = p.user
        s = Savour()
        time_recipe = Time(prep_time=10, cook_time=10)
        step = Step(text="Step", image=None)
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=[],
                   serves="2", language=l, temporality="Spring", nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al no haber ingredientes.\n")
        except ValidationError as v:
            pass

    # Prueba numero 13 -- OK
    def test_recipe_ingredients_list_with_none_items(self):
        md = datetime(2014, 4, 10)
        b = datetime(2010, 10, 10)
        u = User.objects.create_user('juan', 'juanmacias@gmail.com', '1234')
        f = Following(display_name="juan", username="juan", user=u)
        t = Tastes(salty=5, sour=20, bitter=8, sweet=7, spicy=7)
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        p = Profile(display_name="juan" ,main_language="English", website="http://www.facebook.com/juanmacias",  tastes=t, user=u,modification_date= md, gender = "f", avatar= "images/i100236495_91881_5.jpg",birth_date =b,location = "Sevilla",additional_languages = [], following = [f])
        p.save()

        a = p.user
        s = Savour()
        time_recipe = Time(prep_time = 10, cook_time = 10)
        step = Step(text="Step", image=None)
        l = "es"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=["Oil", None],
                   serves="2", language=l, temporality="Spring", nationality="Spain", difficult=2,
                   steps=[step], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=time_recipe, pictures=[], main_image=m)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba en test de ingrediente nulo.\n")
        except ValidationError as v:
            pass

    # Hay que anadir esta prueba al listado -- OK
    def test_recipe_main_image_null(self):
        a = User.objects.create_user("ricky", "ricky@gmail.com", "rickytaun")
        s = Savour()
        l = "es"
        t = Time(prep_time=20, cook_time=10)
        p = Picture(image="http://juanmanuellopezpazos.appspot.com/photo.jpg")
        step1 = Step(text="Paso 1")
        step2 = Step(text="Paso 2")
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality="Spring", nationality="Spain", difficult=2,
                   steps=[step1, step2], author=a, tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p], main_image=None)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    # Prueba numero 7 -- OK
    def test_recipe_any_savour_out_of_range(self):
        s = Savour(salty=500, sour=10, bitter=10, sweet=20, spicy=15)
        t = Time(prep_time=20, cook_time=10)
        p = Picture(image="http://juanmanuellopezpazos.appspot.com/photo.jpg")
        u = User.objects.create_user("ricky", "ricky@gmail.com", "rickytaun")
        step1 = Step(text="Paso 1")
        step2 = Step(text="Paso 2")
        l = "es"
        m = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality="Spring", nationality="Spain", difficult=2,
                   steps=[step1, step2], tags=[], notes="Nota", special_conditions=[],
                   savours=s, food_type="breakfast", time=t, pictures=[p], main_image=m, author=u)
        try:
            r.clean_fields()
            r.savours.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba.\n")
        except ValidationError as v:
            pass

    # Prueba numero 5 -- OK
    def test_recipe_procedure_with_any_empty_step(self):
        a = User.objects.create_user("ricky", "ricky@gmail.com", "rickytaun")
        s = Savour(salty=50, sour=10, bitter=10, sweet=20, spicy=15)
        step1 = Step(text="")
        step2 = Step(text=" ")
        t = Time(prep_time=20, cook_time=10)
        l = "es"
        p1 = Picture(image="http://juanmanuellopezpazos.appspot.com/photo.jpg")
        p2 = "http://juanmanuellopezpazos.appspot.com/photo.jpg"
        r = Recipe(title="receta de prueba", description="descripcion de la receta", ingredients=['tomate'],
                   serves="2", language=l, temporality="Spring", nationality="Spain", difficult=2,
                   steps=[step1, step2], tags=[], notes="Nota", special_conditions=[], author=a,
                   savours=s, food_type="breakfast", time=t, pictures=[p1], main_image=p2)
        try:
            r.clean_fields()
            r.save()
            self.fail("==>La excepcion no ha saltado como se esperaba al tener pasos vacios.\n")
        except ValidationError as v:
            pass