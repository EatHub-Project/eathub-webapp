# coding=utf-8
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate

from django.template import loader, RequestContext
from webapp.forms import NewAccountForm
from django.forms.util import ErrorList

from webapp.models import Profile, Location, Tastes

from django.core.urlresolvers import reverse


def main(request):
    return HttpResponse("welcome")


def new_account(request):
    #TODO if user is authenticated redirect to main
    if request.method == 'POST':
        form = NewAccountForm(request.POST, request.FILES)
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
            avatar = request.FILES['avatar']

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
                avatar.name=str(p.id) + '.png'
                p.avatar=avatar
                p.save()
                u = authenticate(username=username, password=password)
                login(request, u)
                return HttpResponseRedirect(reverse('main'))  # Redirect after POST

    else:
        form = NewAccountForm()

    return render(request, 'webapp/newaccount.html', {'form': form})


