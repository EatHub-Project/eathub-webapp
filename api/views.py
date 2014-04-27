from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, RecipeSerializer
from webapp.models import Recipe


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Recipe.objects.all()
        serializer_class = RecipeSerializer

