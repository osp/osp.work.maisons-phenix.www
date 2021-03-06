from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

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
    url(r'^', include('aawiki.urls')),
    url(r'^timeline/$', TemplateView.as_view(template_name='timeline.html'),  name='timeline'),
    url(r'^layers/$', TemplateView.as_view(template_name='layers.html'),  name='layers'),
    url(r'^nomenclature/$', TemplateView.as_view(template_name='nomenclature.html'),  name='nomenclature'),
    url(r'^cartouche/$', TemplateView.as_view(template_name='cartouche.html'),  name='cartouche'),
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
