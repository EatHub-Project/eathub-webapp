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



