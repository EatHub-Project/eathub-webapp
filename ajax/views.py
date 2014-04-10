# coding=utf-8
from ajax.forms import ImageUploadForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render
from django.core.files import File
from ajax.models import UploadedImage
import json
from webapp.models import Following
from webapp.models import Recipe, Vote
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


def test(request):
    return render(request, 'ajax/follow.html', )


def upload_picture(request):
    f = request.FILES['image']
    img = UploadedImage(image=f)
    img.save()
    return HttpResponse(json.dumps({"id": img.id, "url": img.image.url}))


def follow(request):
    # Saco el usuario actual, y me aseguro de que esté logueado
    me = request.user
    if not me.is_authenticated():
        return HttpResponse(json.dumps({"message": "No user logued in"}), status=403)
    my_profile = me.profile.get()

    # Saco de la petición el usuario al que se le quiere seguir
    username = request.POST['username']
    if not username:
        return HttpResponse(json.dumps({"message": "You must specify a user to follow by its username"}), status=400)
    try:
        who = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"message": "Invalid username"}), status=400)

    # Compruebo si ya está en mi lista de seguidos
    #TODO: INEFICIENTE, habría que hacer una búsqueda de verdad en la bbdd, pero ahora mismo no sé cómo se haría
    following_now = my_profile.following
    for f in following_now:
        if f.user.id == who.id:
            return HttpResponse(json.dumps({"message": "You are already following " + who.username}), status=400)

    # Lo añado a mi lista
    following_now.append(Following.create_following(who))
    my_profile.save()

    # Y respondo con un ok

    return HttpResponse(json.dumps({"message": "OK"}), status=200)


def unfollow(request):
    # Saco el usuario actual, y me aseguro de que esté logueado
    me = request.user
    if not me.is_authenticated():
        return HttpResponse(json.dumps({"message": "No user logued in"}), status=403)
    my_profile = me.profile.get()

    # Saco de la petición el usuario al que se le quiere dejar de seguir
    username = request.POST['username']
    if not username:
        return HttpResponse(json.dumps({"message": "You must specify a user to follow by its username"}), status=400)
    try:
        who = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"message": "Invalid username"}), status=400)

    # Compruebo que está en mi lista de seguidos
    #TODO: INEFICIENTE, habría que hacer una búsqueda de verdad en la bbdd, pero ahora mismo no sé cómo se haría
    following_now = my_profile.following
    for f in following_now:
        if f.user.id == who.id:
            # Dejo de seguirlo
            following_now.remove(f)
            my_profile.save()
            return HttpResponse(json.dumps({"message": "OK"}), status=200)

    return HttpResponse(json.dumps({"message": "You are not following " + who.username}), status=400)


def vote_recipe(request):
    # Compruebo que el usuario actual este logeado
    ppal = request.user
    if not ppal.is_authenticated():
        return HttpResponse(json.dumps({"message":"No user logged in"}), status=403)

    # Comprobacion previa y carga de los datos de la peticion

    # Compruebo que se ha especificado un id y que existe una receta con ese id
    recipe_id = request.POST['recipe']
    if not recipe_id:
        return HttpResponse(json.dumps({"message": "You must specify a recipe to vote by its id"}), status=400)

    try:
        recipe = Recipe.objects.get(id=recipe_id)
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

def recipe_votes(request, recipe_id):
    if recipe_id == u'':
        return HttpResponse(json.dumps({"message": "ERROR: you must specify recipe id"}), status=400)

    recipe = Recipe.objects.get(id=recipe_id)

    return HttpResponse(json.dumps({"positives": len(recipe.positives), "negatives": len(recipe.negatives)}), status=200)