from django.conf.urls import patterns, url
from ajax import views


urlpatterns = patterns('',

    url(r'^test/$', views.test, name='test'),
    url(r'^upload/$', views.upload_picture, name='upload'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^unfollow/$', views.unfollow, name='unfollow'),
    url(r'^vote/$', views.vote_recipe, name='vote'),
)