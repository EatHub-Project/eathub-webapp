from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),

    # Login / Register
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^acount/new/$', views.new_account, name='newaccount'),
    url(r'^account/activate/(?P<code>.+)/$', views.activate_account, name='activate'),
    url(r'^newaccount_done/(?P<username>.+)/$', views.new_account_done, name='newaccount_done'),

    # Profile
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>\w+)/edit/$', views.modification_account, name='profile_edit'),
    url(r'^profile/(?P<username>\w+)/following/$', views.following, name='following'),
    url(r'^profile/(?P<username>\w+)/followers/$', views.followers, name='followers'),
    url(r'^profile/(?P<username>\w+)/recipes/$' , views.recipes, name='recipes'),

    # Recipes
    url(r'^newrecipe', views.new_recipe, name='newrecipe'),
    url(r'^recipe/(?P<recipe_id>\w+)/$' , views.receta, name='recipe'),
    url(r'^recipe/(?P<recipe_id>\w+)/edit/$' , views.edit_receta, name='editrecipe'),
    url(r'^recipe/(?P<recipe_id>\w+)/clone/$' , views.edit_receta, {"clone": True}, name='clonerecipe'),
    url(r'^recipe/(?P<recipe_id>\w+)/comment/$' , views.comment, name='comment'),
    url(r'^recipe/(?P<recipe_id>\w+)/comment/(?P<comment_id>\w+)/ban/$' , views.ban_comment, name='ban'),
    url(r'^recipe/(?P<recipe_id>\w+)/comment/(?P<comment_id>\w+)/unban/$' , views.unban_comment, name='unban'),

    # Search
    url(r'^search/$' , views.search, name='search'),

    # About
    url(r'^termsandconditions/$', views.terms_and_conditions, name='terms_and_conditions'),
    url(r'^about/contact/$', views.contact, name='contact'),
    url(r'^about/team/$', views.about_team, name='about_team'),
)