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

    #check if list fields are lists and if they are not transform them into a list
    aux = recipe.pictures
    recipe.pictures = __makeListField(aux)
    aux = recipe.special_conditions
    recipe.special_conditions = __makeListField(aux)
    aux = recipe.steps
    recipe.steps = __makeListField(aux)
    aux = recipe.tags
    recipe.tags = __makeListField(aux)
    aux = recipe.temporality
    recipe.temporality = __makeListField(aux)

    template = loader.get_template('webapp/recipe_template.html')
    context = RequestContext(request, {
        'receta': recipe
    })

    return HttpResponse(template.render(context))

# Ancillary methods ------------------------------------------------------------------------------------------
def __makeListField(field):
    '''
     Checks if field is a list and if it isn't transform it into a list.

     Since none of the ListFields used in our model is expected to be a list of elements
     with length 1 if the first element of the ListField has that length the list
     is considered to be a decomposed string
    '''

    res = ""

    if len(field)>0 and len(field[0])==1:
        for char in field:
            res+=char
    else:
        res = field

    return res
