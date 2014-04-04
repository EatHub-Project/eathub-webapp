from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),
    url(r'^newaccount/$', views.new_account, name='newaccount'),
    url(r'^profile/(?P<username>\w+)/edit/$', views.modification_account, name='profile_edit'),
    url(r'^newrecipe', views.new_recipe, name='newrecipe'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^private/$', views.test_login_required, name='private'),
    url(r'^recipe/(?P<recipe_id>\w+)/$' , views.receta, name='recipe'),
	url(r'^profile/(?P<username>\w+)$', views.profile, name='profile'),
)