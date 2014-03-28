# coding=utf-8
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login

from django.template import loader, RequestContext
from webapp.forms import NewAccountForm

from webapp.models import Recipe, Profile


def main(request):
    return HttpResponse("welcome")


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

            u = User.objects.create_user(username, email, password)
            p = Profile(display_name=display_name, main_language=main_language, user=u)
            p.save()  # TODO borrar el User si falla al guardar el perfil

            login(request, u)
            return HttpResponseRedirect(reverse('main'))  # Redirect after POST

    else:
        form = NewAccountForm()

    return render(request, 'webapp/newaccount.html', {'form': form})


