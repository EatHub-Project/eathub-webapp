from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^recipe/(?P<recipe_id>\w+)/$' , views.receta, name='recipe'),
)