from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from requests import HTTPError
from rest_framework import viewsets
from api.serializers import UserSerializer, RecipeSerializer
from sorl.thumbnail import get_thumbnail
from webapp.models import Recipe


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all().order_by('-creation_date')
    serializer_class = RecipeSerializer


def resize(request, url, width, height, quality, cached):
    try:
        if int(height) < 0:
            size = width
            crop = "noop"
            upscale = False
        else:
            size = width + "x" + height
            crop = "center"
            upscale = True
        im = get_thumbnail(url, size, crop=crop, quality=int(quality), upscale=upscale)
        if cached == "cached":
            return HttpResponseRedirect(im.url)
        else:
            # Nota: no funciona si se usa como almacenamiento Amazon S3.
            uri = "." + im.url
            with open(uri, "rb") as f:
                return HttpResponse(f.read(), mimetype="image/jpeg")
    except (HTTPError, IOError):
        return HttpResponseNotFound()