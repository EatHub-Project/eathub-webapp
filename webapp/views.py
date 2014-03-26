from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from django.template import loader
from django.views.generic.edit import CreateView

from webapp.models import Recipe

from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from webapp.models import User
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import messages
from django.utils.translation import gettext




def lista_recetas(request):
    recetas = Recipe.objects.all()
    template = loader.get_template('webapp/recipe_list_template.html')
    context = RequestContext(request, {
        'recetas': recetas
    })
    return HttpResponse(template.render(context))


user = None


def login_user(request):
    global user
    logout(request)
    username = password = ''

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if user is None:
            #args = {}
            #args.update(csrf(request))
            errormessage = gettext("Check your credentials")
            messages.error(request, errormessage)

            #return render_to_response('login.html', args)

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            #request.session['username'] = username
            #request.session['password'] = password
            return HttpResponseRedirect('/main/')
    return render_to_response('login.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def main(request):
    global user
    if user is None:
        return render_to_response('login.html', context_instance=RequestContext(request))
    return render_to_response('main.html', {'username':user.username, 'password':user.password})