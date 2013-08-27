from django.conf.urls import include, patterns, url
from tastypie.api import Api
from aawiki.views import ResourceListView, ResourceDetailView, AnnotationUpdateView, AnnotationUpdateSuccessView
from aawiki.api import ResourceResource, AnnotationResource


v1_api = Api(api_name='v1')
v1_api.register(AnnotationResource())
v1_api.register(ResourceResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^resources/$', ResourceListView.as_view(), name='resource-list'),
    url(r'^resources/(?P<pk>\d+)/$', ResourceDetailView.as_view(), name='resource-detail'),
    url(r'^annotations/(?P<pk>\d+)/update/$', AnnotationUpdateView.as_view(), name='annotation-update'),
    url(r'^annotations/update/success/$', AnnotationUpdateSuccessView.as_view(), name='annotation-update-success')
)
