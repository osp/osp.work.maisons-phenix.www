from django.conf.urls import patterns, include, url
from django.views.generic import DetailView
from models import Sound


urlpatterns = patterns('collection.views',
    url(r'^convert/(?P<id>\d+)/', 'convert', name="convert"),
    url(r'^sound_list/$', 'sound_list'),
    url(r'^points/$', 'points'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Sound), name='sound-detail'),
)
