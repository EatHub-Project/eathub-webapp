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
    url(r'^recipe/(?P<recipe_id>.+)/$' , views.receta, name='recipe'),
    url(r'^recipe/(?P<recipe_id>.+)/edit/$' , views.edit_receta, name='editrecipe'),
    url(r'^recipe/(?P<recipe_id>.+)/clone/$' , views.edit_receta, {"clone": True}, name='clonerecipe'),
	url(r'^profile/(?P<username>.+)$', views.profile, name='profile'),
	url(r'^following/(?P<username>.+)$', views.following, name='following'),
    url(r'^followers/(?P<username>.+)$', views.followers, name='followers'),
    url(r'^recipe/(?P<recipe_id>.+)/comment/$' , views.comment, name='comment'),
    url(r'^recipe/(?P<recipe_id>.+)/comment/(?P<comment_id>\w+)/banned/$' , views.banned_comment, name='banned'),
    url(r'^recipe/(?P<recipe_id>.+)/comment/(?P<comment_id>\w+)/unbanned/$' , views.unbanned_comment, name='unbanned'),
    url(r'^recipes/(?P<username>.+)$' , views.recipes, name='recipes'),
)