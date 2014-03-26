from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from django.template import loader, RequestContext
from django.views.generic.edit import CreateView

from webapp.models import Recipe


def lista_recetas(request):
    recetas = Recipe.objects.all()
    template = loader.get_template('webapp/recipe_list_template.html')
    context = RequestContext(request, {
        'recetas': recetas
    })
    return HttpResponse(template.render(context))
