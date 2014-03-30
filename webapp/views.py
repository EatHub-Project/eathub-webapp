from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader, RequestContext

from webapp.models import Recipe


def lista_recetas(request):
    recetas = Recipe.objects.all()
    template = loader.get_template('webapp/recipe_list_template.html')
    context = RequestContext(request, {
        'recetas': recetas
    })
    return HttpResponse(template.render(context))

# Create your views here.
def receta(request):
    recipe_id = request.GET.get('id','')
    recipe = Recipe.objects.get(id=recipe_id)

    template = loader.get_template('webapp/recipe_template.html')
    context = RequestContext(request, {
        'receta': recipe
    })

    return HttpResponse(template.render(context))

# Ancillary methods ------------------------------------------------------------------------------------------
