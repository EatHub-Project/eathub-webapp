# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from webapp.models import Profile, Location, Tastes

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from webapp.forms import NewAccountForm, EditAccountForm
from django.forms.util import ErrorList


def main(request):
    if request.user.is_authenticated():
        return HttpResponse("Welcome, " + request.user.username)
    else:
        return HttpResponse("Welcome to EatHub, guest")


def new_account(request):
    #TODO if user is authenticated redirect to main
    if request.method == 'POST':
        form = NewAccountForm(request.POST)
        if form.is_valid():  # else -> render respone with the obtained form, with errors and stuff
            # Extract the data from the form and create the User and Profile instance
            # TODO validar que el nombre de usuario sea único
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password_repeat = data['password_repeat']

            display_name = data['display_name']
            main_language = data['main_language']

            additional_languages = data['additional_languages']
            gender = data['gender']
            country = data['country']
            city = data['city']
            website = data['website']
            birth_date = data['birth_date']

            if not password == password_repeat:
                errors = form._errors.setdefault("password_repeat", ErrorList())
                errors.append(u"Passwords don't match")

            elif User.objects.filter(username=username).count():
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(u"Username alerady taken")
            #todo: validar email único también
            else:
                u = User.objects.create_user(username, email, password)
                t = Tastes(salty=data['salty'],
                           sour=data['sour'],
                           bitter=data['bitter'],
                           sweet=data['sweet'],
                           spicy=data['spicy'])
                p = Profile(display_name=display_name, main_language=main_language, user=u,
                            additional_languages=additional_languages, gender=gender,
                            location=Location(country=country, city=city), website=website,
                            birthDate=birth_date, tastes=t)
                #TODO capturar cualquier error de validación y meterlo como error en el formulario
                p.clean()
                p.save()  # TODO borrar el User si falla al guardar el perfil
                u = authenticate(username=username, password=password)
                login(request, u)
                return HttpResponseRedirect(reverse('main'))  # Redirect after POST

    else:
        form = NewAccountForm()

    return render(request, 'webapp/newaccount.html', {'form': form})


@login_required
def modification_account(request):
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
            # TODO comparar las contraseñas y dar error si no son iguales

            display_name = data['display_name']
            main_language = data['main_language']

            additional_languages = data['additional_languages']
            gender = data['gender']
            country = data['country']
            city = data['city']
            website = data['website']
            birth_date = data['birth_date']

            if password:  # todo comprobar también que sea válida en cuanto a caracteres y tal
                if not password == password_repeat:
                    errors = form._errors.setdefault("password_repeat", ErrorList())
                    errors.append(u"Passwords don't match")
                    valid = False

            u = request.user
            p = u.profile.get()

            t = Tastes(salty=data['salty'],
                       sour=data['sour'],
                       bitter=data['bitter'],
                       sweet=data['sweet'],
                       spicy=data['spicy'])

            p.display_name = display_name
            p.main_language = main_language
            p.additional_languages = additional_languages
            p.gender = gender
            p.website = website
            p.location = Location(country=country, city=city)
            p.birthDate = birth_date
            p.tastes = t

            if password:
                u.set_password(password)

            # TODO capturar cualquier error de validación y meterlo como error en el formulario
            p.clean()
            if valid:
                p.save()
                u.save()
                # TODO mandar a la misma página y mostrar un mensaje de éxito
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
            'country': p.location.country,
            'city': p.location.city,
            'website': p.website,
            'birth_date': p.birthDate,
            'salty': p.tastes.salty,
            'sour': p.tastes.sour,
            'bitter': p.tastes.bitter,
            'sweet': p.tastes.sweet,
            'spicy': p.tastes.spicy,
        }
        form = EditAccountForm(initial=data)

    return render(request, 'webapp/newaccount.html', {'form': form, 'edit': True})


def login_user(request):
    # Usa la Authentication View:
    # https://docs.djangoproject.com/en/1.5/topics/auth/default/#module-django.contrib.auth.views
    return views.login(request, 'webapp/login.html')


def logout_user(request):
    # TODO: estaría bien mostrar una página de logout correcto, o un mensaje en la principal
    return views.logout(request, next_page=reverse('main'))


@login_required
def test_login_required(request):
    return HttpResponse("Secret, " + request.user.username)