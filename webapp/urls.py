from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.lista_recetas, name='index'),
    url(r'^recipe/', views.receta, name='recipe'),
)