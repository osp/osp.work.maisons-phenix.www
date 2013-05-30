from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from models import Sound


urlpatterns = patterns('collection.views',
    url(r'^convert/(?P<id>\d+)/', 'convert', name="convert"),
    url(r'^sound_list/$', 'sound_list'),
    url(r'^points/$', 'points'),
    url(r'^$', ListView.as_view(model=Sound), name='sound-list'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Sound), name='sound-detail'),
)
