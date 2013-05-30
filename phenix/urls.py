from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns = patterns('',
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#) + staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^djcelery/', include('djcelery.urls')),
    url(r'^aacore/', include('aacore.urls')),
    url(r'^', include('collection.urls')),
)

if settings.DEBUG:
    baseurlregex = r'^static/(?P<path>.*)$'
    urlpatterns += patterns('',
        (baseurlregex, 'django.views.static.serve',
        {'document_root':  settings.MEDIA_ROOT}),
    )

    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
