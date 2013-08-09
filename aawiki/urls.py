from django.conf.urls import include, patterns, url
from tastypie.api import Api
from aawiki.views import ResourceDetailView
from aawiki.api import ResourceResource, AnnotationResource


v1_api = Api(api_name='v1')
v1_api.register(AnnotationResource())
v1_api.register(ResourceResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^(?P<pk>\d+)/$', ResourceDetailView.as_view(), name='resource-detail'),
)
