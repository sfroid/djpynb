from django.conf.urls import patterns, url
from reddit import views

urlpatterns = patterns('',
    url(r'^api/v1/(?P<path>.*)$', views.api_v1, name='api_v1'),
    url(r'^(?P<path>.*)$', views.home, name='home'),
)