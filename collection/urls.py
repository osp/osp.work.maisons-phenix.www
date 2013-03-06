from django.conf.urls import patterns, include, url

urlpatterns = patterns('collection.views',
    url(r'^convert/(?P<id>\d+)/', 'convert', name="convert"),
    url(r'^$', 'sound_list'),
)
