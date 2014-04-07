from ajax.forms import ImageUploadForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
from ajax.models import UploadedImage
import json
from webapp.models import Recipe, Vote
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


def test(request):
    form = ImageUploadForm()
    return render(request, 'ajax/upload_image.html', {"form": form})


def upload_picture(request):
    f = request.FILES['image']
    img = UploadedImage(image=f)
    img.save()
    return HttpResponse(json.dumps({"id": img.id, "url": img.image.url}))

def vote_recipe(request):
    # Compruebo que el usuario actual este logeado
    ppal = request.user
    if not ppal.is_authenticated():
        return HttpResponse(json.dumps({"message":"No user logged in"}), status=403)

    # Comprobacion previa y carga de los datos de la peticion

    # Compruebo que se ha especificado un id y que existe una receta con ese id
    id = request.POST['recipe']
    if not id:
        return HttpResponse(json.dumps({"message": "You must specify a recipe to vote by its id"}), status=400)

    try:
        recipe = Recipe.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"message": "Invalid recipe"}), status=400)

    # Compruebo que se ha especificado un tipo de voto valido y construyo un nuevo voto con el
    vote_type = request.POST['type']
    if not vote_type:
        return HttpResponse(json.dumps({"message": "You must specify a vote type (positive or negative)"}), status=400)
    if vote_type != u'positive' and vote_type != u'negative':
        return HttpResponse(json.dumps({"message": "You must specify a valid vote type (positive or negative)"}), status=400)

    new_vote = Vote(user=ppal, date=datetime.now())

    # Busco votos preexistentes del usuario a la receta y los elimino cuando sea necesario
    found = False   #used to control when the vote has to be looked for into the lists

    #TODO: refactorizar! los dos bucles for son muy parecidos... se podria extraer un metodo para no repetir codigo?
    if not found:
        for vote in recipe.positives:
            if vote.user == ppal:
                if vote_type == u'positive':
                    return HttpResponse(json.dumps({"message": "already voted, no action is necessary"}), status=200)
                else:
                    recipe.positives.remove(vote)
                    found = True
                    break

    if not found:
        for vote in recipe.negatives:
            if vote.user == ppal:
                if vote_type == u'negative':
                    return HttpResponse(json.dumps({"message": "already voted, no action is necessary"}), status=200)
                else:
                    recipe.negatives.remove(vote)
                    break

    # Almaceno el nuevo voto
    if vote_type == u'positive':
        recipe.positives.append(new_vote)
        recipe.save()
    else:
        recipe.negatives.append(new_vote)
        recipe.save()

    return HttpResponse(json.dumps({"message": "OK"}), status=201)
