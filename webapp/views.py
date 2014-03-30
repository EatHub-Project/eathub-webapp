# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from webapp.models import Profile, Location, Tastes

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from webapp.forms import NewAccountForm
from webapp.forms import ModificationAccountForm
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
            # TODO comparar las contraseñas y dar error si no son iguales

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



def modification_account(request):
    #TODO if user is authenticated redirect to main
    if request.method == 'POST':
        form = ModificationAccountForm(request.POST)
        if form.is_valid():  # else -> render respone with the obtained form, with errors and stuff
            # Extract the data from the form and create the User and Profile instance
            # TODO validar que el nombre de usuario sea único
            data = form.cleaned_data
            username = data['username']
            email = data['email']
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
        form = ModificationAccountForm()

    return render(request, 'webapp/modifytheaccount.html', {'form': form})






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