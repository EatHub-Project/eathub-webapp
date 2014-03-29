from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),
    url(r'newaccount', views.new_account, name='newaccount'),
)