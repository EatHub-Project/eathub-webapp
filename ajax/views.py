from ajax.forms import ImageUploadForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
from ajax.models import UploadedImage
import json
from webapp.models import Recipe, Vote
from datetime import datetime


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
    ppal_profile = ppal.profile.get()

    # Compruebo si el usuario ya ha votado la receta previamente.
    # Si ha votado su voto anterior se sustituye por el nuevo.
    id = request.POST['recipe']
    vote_type = request.POST['type']
    recipe = Recipe.objects.get(id=id)
    new_vote = Vote(user=ppal_profile, date=datetime.now())

    #TODO: refactorizar! los dos bucles for son muy parecidos... se podria extraer un metodo para no repetir codigo?
    for vote in recipe.positives:
        if vote.user is ppal_profile:
            if vote_type is u'positive':
                return HttpResponse(json.dumps({"message": "already voted, no action is necessary"}), status=200)
            else:
                recipe.negatives.remove(vote)
                break

    for vote in recipe.negatives:
        if vote.user is ppal_profile:
            if vote_type is u'negative':
                return HttpResponse(json.dumps({"message": "already voted, no action is necessary"}), status=200)
            else:
                recipe.positives.remove(vote)
                break

    if vote_type is u'positive':
        recipe.positives.append(new_vote)
        recipe.save()
    else:
        recipe.negatives.append(new_vote)
        recipe.save()

    return HttpResponse(json.dumps({"message": "OK"}), status=201)
