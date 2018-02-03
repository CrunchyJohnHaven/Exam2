from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main/$', views.index),
    url(r'^login$', views.login),
    url(r'^reg$', views.reg),
    url(r'^travels/$', views.success),
    url(r'^travels/add$', views.page2),
    url(r'^travels/destination/(?P<id>\d+)$', views.users),
    url(r'^logout$', views.logout),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^create/(?P<id>\d+)$', views.create),
    url(r'^remove/(?P<id>\d+)$', views.remove), 
    url(r'^page1/(?P<id>\d+)$', views.page1),
]
