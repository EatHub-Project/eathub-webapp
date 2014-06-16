# coding=utf-8
import string
import urllib2
from urlparse import urlparse
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q
from django.db.models.query import RawQuerySet
from django.forms import ImageField
from django.templatetags.static import static
from pip._vendor import requests
from ajax import models as models_ajax
from bson import ObjectId
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from webapp.models import Profile, Tastes, Recipe, Comment, Time, Savour, Step, Picture, Activation
from ajax.models import UploadedImage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render

from webapp.forms import NewAccountForm, EditAccountForm, RecipeForm, AddComment, SearchRecipeForm
from django.forms.util import ErrorList
import time, datetime

from social.pipeline.partial import partial
from django.shortcuts import redirect

from django.utils.translation import ugettext as _

#Para el correo
from django.core.mail import send_mail
from django.template import loader

#Para el hash con md5
import hashlib

#full-text
from pymongo import *

def search_recipe(request):
    results_recipes = dict()
    if request.method == 'GET':
        form = SearchRecipeForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            results_recipes = Recipe.search_recipes(data)

    return render(request, 'webapp/search_recipe_result.html', {'matches_recipe': results_recipes, 'results': len(results_recipes), 'form': form})


def search_profile(request, terms):
    if request.method == 'GET':

        client = MongoClient()

        results_profiles = Profile.objects.raw_query({"$text": {"$search" : terms}})

        return render(request, 'webapp/search_person_result.html', {'matches_profile': results_profiles})

def main(request):
    if request.user.is_authenticated():
        if 'django_language' not in request.session:
            request.session['django_language']=request.user.profile.get().main_language
    recipes = Recipe.objects.all().order_by('-creation_date')
    return render(request, 'webapp/main.html', {'recipes': recipes[:9]})

def about(request):
        return render(request, 'webapp/about.html')

def new_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('main'))

    if request.method == 'POST':
        form = NewAccountForm(request.POST)
        if form.is_valid():  # else -> render respone with the obtained form, with errors and stuff
            # Extract the data from the form and create the User and Profile instance
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password_repeat = data['password_repeat']

            display_name = data['display_name']
            main_language = data['main_language']

            additional_languages = data['additional_languages']
            gender = data['gender']
            location = data['location']
            website = data['website']
            birth_date = data['birth_date']

            avatar_id = data['avatar_id']
            if avatar_id != u'':
                avatar = models_ajax.UploadedImage.objects.get(id=avatar_id)

            if not password == password_repeat:
                errors = form._errors.setdefault("password_repeat", ErrorList())
                output = _("Passwords don't match")
                errors.append(unicode(output))

            elif User.objects.filter(username=username).count():
                errors = form._errors.setdefault("username", ErrorList())
                output = _("Username alerady taken")
                errors.append(unicode(output))

            try:
                valid_email = User.objects.get(email=email)
            except :
                valid_email = False

            if valid_email:
                errors = form._errors.setdefault("email", ErrorList())
                output = _("Email alerady exists")
                errors.append(unicode(output))

            else:
                u = User.objects.create_user(username, email, password)
                t = Tastes(salty=data['salty'],
                           sour=data['sour'],
                           bitter=data['bitter'],
                           sweet=data['sweet'],
                           spicy=data['spicy'])
                p = Profile(display_name=display_name, main_language=main_language, user=u,
                            additional_languages=additional_languages, gender=gender,
                            location=location, website=website,
                            birth_date=birth_date, tastes=t, username=username)
                #TODO capturar cualquier error de validación y meterlo como error en el formulario

                #avatar.image.name = str(p.id) + '.png' # No vale así, hay que copiar el archivo en otro
                if avatar_id != u'':
                    p.avatar = avatar.image

                p.user.is_active = False

                p.user.save()

                p.clean()
                p.save()  # TODO borrar el User si falla al guardar el perfil

                #Generar el codigo y meterlo en la BD.

                #TODO marco de el UploadedImage para que no se borre. Pero lo mejor sería copiar la imagen a otro sitio
                if avatar_id != u'':
                    avatar.persist = True
                    avatar.save()

                #return render(request, 'webapp/newaccount_done.html', {'profile': p.user.username})  # Redirect after POST
                return HttpResponseRedirect(reverse('newaccount_done', kwargs={'username': p.user.username}))

    else:
        form = NewAccountForm()

    return render(request, 'webapp/newaccount.html', {'form': form})


def activate_account(request, code):
    try:
        a = Activation.objects.get(code=code)
    except Activation.DoesNotExist:
        raise Http404

    if a.user.is_active:
        return HttpResponseRedirect(reverse('main'))

    a.user.is_active = True
    a.user.save()

    messages.success(request, _("Your account has been successfully activated. You can log in now."))
    return HttpResponseRedirect(reverse('login'))


def new_account_done(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    #TODO: esto hay que cambiarlo para que se haga por post, y que muestre un mensaje mas concreto. De momento asi estaria eliminado el bug.
    if user.is_active:
        return HttpResponseRedirect(reverse('main'))

    ts = time.time()
    now_datetime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    while True:
        hash = hashlib.md5()
        hash.update(username)
        hash.update(str(now_datetime))
        hash.digest()
        if not Activation.objects.filter(code=hash.hexdigest()).exists():
            break

    a = Activation(user=user, code=hash.hexdigest(), date=now_datetime)
    a.save()

    context = {
            'site': request.get_host(),
            'user': user,
            'username': username,
            'token': a.code,
            'secure': request.is_secure(),
        }
    body = loader.render_to_string("email/activation_email.txt", context).strip()
    subject = loader.render_to_string("email/activation_email_subject.txt", context).strip()
    send_mail(subject, body, "eathub.contact@gmail.com", [user.email])

    #enviar el mail.
    return render(request, 'webapp/newaccount_done.html', {}) #pasar profile para mostrar datos en pantallas


@login_required
def new_recipe(request):
    #TODO if user is authenticated redirect to main
    if request.method == 'POST':
        # else -> render respone with the obtained form, with errors and stuff
        form = RecipeForm(request.POST)
        if form.is_valid:  # else -> render respone with the obtained form, with errors and stuff
            recipe = store_recipe(form, request.user)
            if recipe:
                return HttpResponseRedirect(reverse('recipe', kwargs={'recipe_id': recipe.id}))  # Redirect after POST
    else:
        form = RecipeForm()

    return render(request, 'webapp/newrecipe.html', {'form': form})


@login_required
def edit_receta(request, recipe_id, clone=False):
    user = request.user
    r = Recipe.objects.get(id=ObjectId(recipe_id))

    if not clone and r.author != user:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid:  # else -> render respone with the obtained form, with errors and stuff
            if clone:
                recipe = store_recipe(form, request.user, parent=r)
            else:
                recipe = store_recipe(form, request.user, r)

            if recipe:
                return HttpResponseRedirect(reverse('recipe', kwargs={'recipe_id': recipe.id}))  # Redirect after POST

    else:
        # fill the form with the recipe's data
        form = RecipeForm.get_filled_form(r)
        return render(request, 'webapp/newrecipe.html', {'form': form, 'edit': True})


def store_recipe(form, user, recipe=None, parent=None):
    if form.is_valid():
        # Extract the data from the form and create the User and Profile instance
        data = form.cleaned_data

        # Basic information
        title = data['title']
        description = data['description']
        main_picture = data['main_picture_id']

        pictures_id_list = form.get_pictures_ids_list()
        ingredients = form.get_ingredients_list()
        steps = form.get_steps_list()

        serves = data['serves']
        language = data['language']
        temporality = data['temporality']
        nationality = data['nationality']
        special_conditions = data['special_conditions']
        notes = data['notes']
        difficult = data['difficult']
        food_type = data['food_type']
        tags = []
        tags_all = data['tags']
        prep_time = data['prep_time']
        cook_time = data['cook_time']
        if tags_all:
            tags = tags_all.split(",")

        # Genera la receta
        t = Savour(salty=data['salty'],
                   sour=data['sour'],
                   bitter=data['bitter'],
                   sweet=data['sweet'],
                   spicy=data['spicy'])

        time = Time(prep_time=prep_time, cook_time=cook_time)
        imagen_principal = UploadedImage.objects.get(id=main_picture).image

        if not recipe:
            recipe = Recipe()
        if parent:
            recipe.parent = parent

        recipe.title = title
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.serves = serves
        recipe.language = language
        recipe.temporality = temporality
        recipe.nationality = nationality
        recipe.special_conditions = special_conditions
        recipe.notes = notes
        recipe.difficult = difficult
        recipe.food_type = food_type
        recipe.tags = tags
        recipe.main_image = imagen_principal
        u = user

        # steps is a list of dict
        step_list = list()
        for step in steps:
            if "picture" in step:
                picture = UploadedImage.objects.get(id=step["picture"]).image
                step_object = Step(text=step['text'], image=picture)
            else:
                step_object = Step(text=step['text'])

            step_list.append(step_object)
        recipe.steps = step_list

        # pictures_id_list is a list of ids
        pictures_list = list()
        if pictures_id_list:
            for pic in pictures_id_list:
                if pic:
                    picture = Picture(image=UploadedImage.objects.get(id=pic).image)
                    pictures_list.append(picture)

        recipe.pictures = pictures_list
        recipe.savours = t
        recipe.time = time
        recipe.author = u
        recipe.clean()
        recipe.save()
        return recipe
    else:
        return None


@login_required
def modification_account(request, username):
    # todo: hay mucho código repetido con respecto a la vista new_account. ¿Se pueden simplificar?
    if request.method == 'POST':
        form = EditAccountForm(request.POST)
        if form.is_valid():  # else -> render respone with the obtained form, with errors and stuff
            valid = True
            # Extract the data from the form, validate, and update the current user
            # TODO validar que el nombre de usuario sea único
            data = form.cleaned_data
            #username = data['username']
            #email = data['email']
            password = data['password']
            password_repeat = data['password_repeat']

            display_name = data['display_name']
            main_language = data['main_language']

            additional_languages = data['additional_languages']
            gender = data['gender']
            location = data['location']
            website = data['website']
            birth_date = data['birth_date']

            avatar_id = data['avatar_id']

            if password:  # todo comprobar también que sea válida en cuanto a caracteres y tal
                if not password == password_repeat:
                    errors = form._errors.setdefault("password_repeat", ErrorList())
                    output = _("Passwords don't match")
                    errors.append(unicode(output))
                    valid = False

            u = request.user
            p = u.profile.get()

            t = Tastes(salty=data['salty'] if data['salty'] != None else 0,
                       sour=data['sour'] if data['sour'] != None else 0,
                       bitter=data['bitter'] if data['bitter'] != None else 0,
                       sweet=data['sweet'] if data['sweet'] != None else 0,
                       spicy=data['spicy'] if data['spicy'] != None else 0)

            p.display_name = display_name
            p.main_language = main_language
            p.additional_languages = additional_languages
            p.gender = gender
            p.website = website
            p.location = location
            p.birth_date = birth_date
            p.tastes = t

            if password:
                u.set_password(password)

            avatar = None
            if avatar_id:
                avatar = models_ajax.UploadedImage.objects.get(id=avatar_id)
                if avatar.image:
                    p.avatar = avatar.image
            # TODO capturar cualquier error de validación y meterlo como error en el formulario

            if valid:
                u.save()
                p.clean()
                p.save()  # TODO borrar el User si falla al guardar el perfil

                #TODO marco de el UploadedImage para que no se borre. Pero lo mejor sería copiar la imagen a otro sitio
                if avatar:
                    avatar.persist = True
                    avatar.save()
                # TODO mandar a la misma página y mostrar un mensaje de éxito

                if request.user.is_authenticated():
                    request.session['django_language']=main_language

                return HttpResponseRedirect(reverse('main'))  # Redirect after POST

    else:
        u = request.user
        p = u.profile.get()
        data = {
            'username': u.username,
            'email': u.email,
            'display_name': p.display_name,
            'main_language': p.main_language,
            'additional_languages': p.additional_languages,
            'gender': p.gender,
            'location': p.location,
            'website': p.website,
            'birth_date': p.birth_date,
            'salty': p.tastes.salty,
            'sour': p.tastes.sour,
            'bitter': p.tastes.bitter,
            'sweet': p.tastes.sweet,
            'spicy': p.tastes.spicy,
        }
        if p.avatar:
            data['avatar_url']=p.avatar.url
        else:
            data['avatar_url']=static("webapp/image/profile_pic_anon.png")
        form = EditAccountForm(initial=data)

    return render(request, 'webapp/newaccount.html', {'form': form, 'edit': True})


def login_user(request):
    # Usa la Authentication View:
    # https://docs.djangoproject.com/en/1.5/topics/auth/default/#module-django.contrib.auth.views
    return views.login(request, 'webapp/login.html')


def logout_user(request):
    # TODO: estaría bien mostrar una página de logout correcto, o un mensaje en la principal
    return views.logout(request, next_page=reverse('main'))

#TODO: mover a otro fichero e importar
def calculate_affinity(friend_profile, recipe):
    ret_affinity = 0

    ret_affinity = (
        abs(friend_profile.tastes.bitter - recipe.savours.bitter) +
        abs(friend_profile.tastes.salty - recipe.savours.salty) +
        abs(friend_profile.tastes.sour - recipe.savours.sour) +
        abs(friend_profile.tastes.spicy - recipe.savours.spicy) +
        abs(friend_profile.tastes.sweet - recipe.savours.sweet)
                   )/5

    return 100-ret_affinity

def affinity(request, username, recipe_id):
    try:
        user = User.objects.get(username=username)
        recipe = Recipe.objects.get(id=recipe_id)
    except User.DoesNotExist:
        raise Http404

    user_profile = Profile.objects.get(user=user)

    affinity = calculate_affinity(user_profile, recipe)

    return render(request, 'webapp/affinity.html', {'user_profile': user_profile,'recipe': recipe, 'affinity': affinity})


def receta(request, recipe_id):

    following = None
    if request.user.is_authenticated():
        #username = request.user.username
        #user = User.objects.get(username=username)
        my_profile = request.user.profile.get()
        following = my_profile.following

    recipe = Recipe.objects.get(id=recipe_id)

    total_votos = len(recipe.positives) + len(recipe.negatives)
    porcentaje_positivos = 50
    porcentaje_negativos = 50
    if total_votos != 0:
        porcentaje_positivos = (len(recipe.positives) / float(total_votos))*100
        porcentaje_negativos = (len(recipe.negatives) / float(total_votos))*100

    lang=django.utils.translation.get_language().split('-')[0]
    recipe.translate_to_language(lang)

    num = recipe.difficult
    dificultad = "Dificil"
    if num>=0 and num<=1:
        dificultad = "Facil"
    elif num>=2 and num<=3:
        dificultad = "Media"

    return render(request, 'webapp/recipe_template.html', {'receta': recipe, 'total_votos': total_votos, 'difficult_value': dificultad,
                                                           'por_pos': int(porcentaje_positivos), 'por_neg': int(porcentaje_negativos),
                                                           'following': following})


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    user_profile = Profile.objects.get(user=user)
    recipes = Recipe.objects.raw_query({'author_id': ObjectId(user.id)})
    followers_list = Profile.objects.raw_query({'following.user_id': ObjectId(user.id)})
    is_owner = False
    if request.user.username == username:
        is_owner = True

    # Compruebo si está en mi lista de seguidos
    is_following = False
    if request.user.is_authenticated() and user.id != request.user.id:
        my_profile = request.user.profile.get()
        #TODO: INEFICIENTE, habría que hacer una búsqueda de verdad en la bbdd, pero ahora mismo no sé cómo se haría
        following_now = my_profile.following
        for f in following_now:
            if f.user.id == user.id:
                is_following = True

    lang=django.utils.translation.get_language().split('-')[0]
    user_profile.translate_to_lengague(lang)

    return render(request, 'webapp/profile.html',
                  {'profile': user_profile, 'following': is_following, 'followers_list': followers_list,
                   'recipes': recipes, 'is_owner': is_owner})


def recipes(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    is_owner = False
    if request.user.username == username:
        is_owner = True

    recipes_list = Recipe.objects.raw_query({'author_id': ObjectId(user.id)}).order_by('-creation_date')
    return render(request, 'webapp/recipes.html', {'recipes': recipes_list, 'is_owner': is_owner})


def following(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    is_owner = False
    if request.user.username == username:
        is_owner = True

    user_profile = Profile.objects.get(user=user)
    tag = _("Following")
    return render(request, 'webapp/following.html',
                  {'follows': user_profile.following, 'profile': user_profile, 'tag': tag, 'is_owner': is_owner})


def followers(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404

    is_owner = False
    if request.user.username == username:
        is_owner = True

    followers_list = Profile.objects.raw_query({'following.user_id': ObjectId(user.id)})
    user_profile = Profile.objects.get(user=user)
    tag = _("Followers")
    return render(request, 'webapp/following.html',
                  {'follows': followers_list, 'profile': user_profile, 'tag': tag, 'is_owner': is_owner})


@login_required
def comment(request, recipe_id):
    if request.method == 'POST':
        u = request.user
        profile = u.profile.get()
        form = AddComment(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            c = Comment(text=text, create_date=datetime.datetime.now(), user_own=u, )
            r = Recipe.objects.get(id=recipe_id)
            r.comments.append(c)
            r.save()
    return HttpResponseRedirect(reverse('recipe', args=(recipe_id,)))


@login_required
def ban_comment(request, recipe_id, comment_id):
    if request.method == 'GET':
        u = request.user
        if u.is_staff:
            r = Recipe.objects.get(id=recipe_id)
            r.comments[int(comment_id)].is_banned = True
            r.save()
    return HttpResponseRedirect(reverse('recipe', args=(recipe_id,)))


@login_required
def unban_comment(request, recipe_id, comment_id):
    if request.method == 'GET':
        u = request.user
        if u.is_staff:
            r = Recipe.objects.get(id=recipe_id)
            r.comments[int(comment_id)].is_banned = False
            r.save()
    return HttpResponseRedirect(reverse('recipe', args=(recipe_id,)))

USER_FIELDS = ['username', 'email', 'first_name']
FACEBOOK_FIELDS = ['link','location', 'gender']
GOOGLE_FIELDS = ['link','picture', 'gender']
@partial
def create_user(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user:
        return {'is_new': False}
    elif strategy.session_pop('is_new'):
        email=strategy.session_pop('user')
        u=User.objects.get(email=email)
        return {'is_new': False,'user':u}


    fields = dict((name, details.get(name))
                        for name in strategy.setting('USER_FIELDS',USER_FIELDS))

    extra_fields = dict()
    if kwargs.get('backend').name=="google-plus":
        extra_fields=dict((name, kwargs.get('response').get(name))
                        for name in strategy.setting('GOOGLE_FIELDS',GOOGLE_FIELDS))
    elif kwargs.get('backend').name=="facebook":
        extra_fields=dict((name, kwargs.get('response').get(name))
                        for name in strategy.setting('FACEBOOK_FIELDS',FACEBOOK_FIELDS))
    fields.update(extra_fields)
    if not fields:
        return
    u = User.objects.create_user(fields.get('username'), email=fields.get('email'))
    t = Tastes(salty=50, sour=50, bitter=50, sweet=50, spicy=50)
    p = Profile()
    p.display_name=fields.get('first_name')
    p.user=u
    p.tastes=t
    p.main_language='es'

    if fields.get('location'):
        p.location=fields.get('location').get('name')

    if fields.get('picture'):
        url=fields.get('picture')
        r = requests.get(url)
        img_temp = NamedTemporaryFile()
        img_temp.write(r.content)
        img_temp.flush()
        name = urlparse(url).path.split('/')[-1]
        upload_image = UploadedImage()
        upload_image.image.save(name, File(img_temp), save=True)
        p.avatar=upload_image.image

    p.clean()
    p.save()

    return {'is_new': False,'user':u}


def terms_and_conditions(request):
    return render(request, 'webapp/terms_and_conditions.html')


def contact(request):
    return render(request, 'webapp/contact.html')


def about_team(request):
    return render(request, 'webapp/about_team.html')

def handle500(request):
    return render(request, '500.html')

def corporative(request):
    team = [
        {
            "name": "Sergio García",
            "position": "Jefe de proyecto",
            "email": "sergaralo@eathub.me",
            "picture": static('webapp/image/staff_sergiog.png'),
            "linkedin": "https://es.linkedin.com/pub/sergio-garcia-alonso/48/979/158/",
            "twitter": "http://twitter.com/sgavmp",
            "gplus": "http://google.com/+SergioGarciaA",
        },
        {
            "name": "David González",
            "position": "Desarrollador",
            "email": "jesgonbel@eathub.me",
            "picture": static('webapp/image/staff_david.png'),
            "linkedin": "https://www.linkedin.com/pub/jes%C3%BAs-david-gonz%C3%A1lez-belda/72/88/b1a",
            "twitter": "http://twitter.com/adlebzelaznog",
            "gplus": "https://plus.google.com/114599300485606375946",
        },
        {
            "name": "Arturo Jiménez",
            "position": "Analista y Tester",
            "email": "artjimlop@eathub.me",
            "picture": static('webapp/image/staff_arturo.png'),
            "linkedin": "https://es.linkedin.com/pub/arturo-jim%C3%A9nez-l%C3%B3pez/89/a8/568",
            "twitter": "http://twitter.com/arturoLehder",
            "gplus": "https://plus.google.com/101478151145229223925",
        },
        {
            "name": "Antonio León",
            "position": "Analista y Tester",
            "email": "antleocar@eathub.me",
            "picture": static('webapp/image/staff_antonio.png'),
            "linkedin": "https://es.linkedin.com/pub/antonio-león-carrillo/99/199/335/",
            "twitter": "http://twitter.com/antbadija",
            "gplus": "https://plus.google.com/+AntonioLeónMH",
        },
        {
            "name": "Juan Manuel López",
            "position": "Desarrollador",
            "email": "jualoppaz@eathub.me",
            "picture": static('webapp/image/staff_juanma.png'),
            "linkedin": "https://es.linkedin.com/pub/juan-manuel-lopez-pazos/63/469/4a9",
            "twitter": "http://twitter.com/LopezPazos14",
            "gplus": "https://plus.google.com/116239751213274580087",
        },
        {
            "name": "Sergio Rodríguez",
            "position": "Desarrollador",
            "email": "serrodcal@eathub.me",
            "picture": static('webapp/image/staff_sergior.png'),
            "linkedin": "https://es.linkedin.com/pub/sergio-rodr%C3%ADguez-calvo/97/b79/38b",
            "twitter": "http://twitter.com/sergio_7rc",
            "gplus": "http://google.com/+SergioRodriguezCalvo",
        },
        {
            "name": "Rafael Vázquez",
            "position": "Jefe de desarrollo",
            "email": "rafvazsan@eathub.me",
            "picture": static('webapp/image/staff_rafa.png'),
            "linkedin": "https://es.linkedin.com/in/sloydev",
            "twitter": "http://twitter.com/sloydev",
            "gplus": "http://google.com/+RafaVazquez",
        },
    ]
    return render(request, 'webapp/corporative.html', {"team": team})

