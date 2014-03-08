from django.conf.urls import patterns, url
from reddit import views

urlpatterns = patterns('',
    url(r'^api/(?P<path>.*)$', views.api, name='api'),
    url(r'^(?P<path>.*)$', views.home, name='home'),
)