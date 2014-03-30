from django.conf.urls import patterns, url
from webapp import views


urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),
    url(r'newaccount', views.new_account, name='newaccount'),
    url(r'modifytheaccount', views.modification_account, name='modifytheaccount'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^private/$', views.test_login_required, name='private'),
)