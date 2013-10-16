from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^djcelery/', include('djcelery.urls')),
    url(r'^aacore/', include('aacore.urls')),
    url(r'^', include('aawiki.urls')),
    url(r'^nomenclature/$', TemplateView.as_view(template_name='nomenclature.html'),  name='nomenclature'),
    url(r'^cartouche/$', TemplateView.as_view(template_name='cartouche.html'),  name='cartouche'),
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
