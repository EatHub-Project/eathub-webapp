# coding=utf-8
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.core.urlresolvers import reverse


def login_user(request):
    # Usa la Authentication View:
    # https://docs.djangoproject.com/en/1.5/topics/auth/default/#module-django.contrib.auth.views
    return views.login(request, 'webapp/login.html')


def logout_user(request):
    # TODO: estaría bien mostrar una página de logout correcto, o un mensaje en la principal
    return views.logout(request, next_page=reverse('main'))


def main(request):
    if request.user.is_authenticated():
        return HttpResponse("Welcome, " + request.user.username)
    else:
        return HttpResponse("Welcome to EatHub, guest")


@login_required
def test_login_required(request):
    return HttpResponse("Secret, " + request.user.username)