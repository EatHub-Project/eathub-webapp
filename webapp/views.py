from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader, RequestContext

from webapp.models import Recipe


# Create your views here.
def receta(request, recipe_id):
    #recipe_id = request.GET.get('id','')
    recipe = Recipe.objects.get(id=recipe_id)

    template = loader.get_template('webapp/recipe_template.html')
    context = RequestContext(request, {
        'receta': recipe
    })

    return HttpResponse(template.render(context))
