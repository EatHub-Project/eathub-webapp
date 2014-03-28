from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),
    url(r'^login/$', views.login_user, name='login'),
)