# coding=utf-8
from api import views
from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User

from rest_framework import viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
from webapp.models import Recipe


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'recipes', views.RecipeViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = patterns('',

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
