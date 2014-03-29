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

# Create your views here.
from django.shortcuts import render_to_response
from webapp.models import Profile
from forms import ProfileForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf




def modificar(request):
    if request.POST:
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')
    else:
        form = ProfileForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('modificar_usuario.html', args)

def receta(request):
    recipe_id = request.GET.get('id','')
    recipe = Recipe.objects.get(id=recipe_id)

    template = loader.get_template('webapp/recipe_template.html')
    context = RequestContext(request, {
        'receta': recipe
    })

    return HttpResponse(template.render(context))