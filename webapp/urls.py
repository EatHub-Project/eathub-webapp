from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),
    url(r'^newaccount/$', views.new_account, name='newaccount'),
    url(r'^newrecipe', views.new_recipe, name='newrecipe'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/(?P<username>.+)/edit/$', views.modification_account, name='profile_edit'),
    url(r'^profile/(?P<username>.+)$', views.profile, name='profile'),
    url(r'^recipe/(?P<recipe_id>\w+)/$' , views.receta, name='recipe'),
	url(r'^profile/(?P<username>\w+)$', views.profile, name='profile'),
	url(r'^following/(?P<username>\w+)$', views.following, name='following'),
    url(r'^followers/(?P<username>\w+)$', views.followers, name='followers'),
    url(r'^recipe/(?P<recipe_id>\w+)/comment/$' , views.comment, name='comment'),
    url(r'^recipe/(?P<recipe_id>\w+)/comment/(?P<comment_id>\w+)/banned/$' , views.banned_comment, name='banned'),
    url(r'^recipe/(?P<recipe_id>\w+)/comment/(?P<comment_id>\w+)/unbanned/$' , views.unbanned_comment, name='unbanned'),
    url(r'^recipes/(?P<username>\w+)/comment/$' , views.recipes, name='recipes'),
)