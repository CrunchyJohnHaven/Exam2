from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.exam2.urls')),
]
