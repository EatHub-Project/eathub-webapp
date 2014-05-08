from PIL import Image
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseNotFound
from requests import HTTPError
from rest_framework import viewsets
from api.serializers import UserSerializer, RecipeSerializer
from sorl.thumbnail import get_thumbnail
from webapp.models import Recipe


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all().order_by('-creation_date')
    serializer_class = RecipeSerializer


def resize(request, url, width, height, quality):
    try:
        im = get_thumbnail(url, width + "x" + height, crop='center', quality=int(quality))
        try:
            uri = "." + im.url
            with open(uri, "rb") as f:
                return HttpResponse(f.read(), mimetype="image/jpeg")
        except IOError:
            red = Image.new('RGBA', (10, 10), (255,0,0,0))
            response = HttpResponse(mimetype="image/jpeg")
            red.save(response, "JPEG")
            return response
    except HTTPError:
        return HttpResponseNotFound()