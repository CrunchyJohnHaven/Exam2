from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main/$', views.index),
    url(r'^login$', views.login),
    url(r'^reg$', views.reg),
    url(r'^quotes/$', views.success),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    #     - url(r'^remove$', views.remove),
    url(r'^create/(?P<id>\d+)$', views.create),
    url(r'^remove/(?P<id>\d+)$', views.remove), 
    url(r'^users/(?P<id>\d+)$', views.users),
]
