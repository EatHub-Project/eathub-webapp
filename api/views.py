from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from requests import HTTPError
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from api.serializers import UserSerializer, RecipeSerializer
from sorl.thumbnail import get_thumbnail
from webapp.forms import SearchRecipeForm
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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def login(request, format=None):
    serializer = UserSerializer(request.user)

    return Response(serializer.data)



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

@api_view(['GET'])
def SearchView(request):
    results_recipes = dict()
    if request.method == 'GET':
        form = SearchRecipeForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            results_recipes = Recipe.search_recipes(data)
    serializer = RecipeSerializer(results_recipes)

    return Response(serializer.data)

