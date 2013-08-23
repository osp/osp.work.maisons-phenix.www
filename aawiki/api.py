from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from aawiki.models import Annotation, Resource
from aawiki.utils.audacity import srt2audacity


class AudacitySerializer(Serializer):
    formats = ['json', 'audacity']
    content_types = {
        'json': 'application/json',
        'audacity': 'text/audacity',
    }
    def to_audacity(self, data, options=None):
        data = self.to_simple(data, options)
        body = data['body']
        return srt2audacity(body)

    def from_audacity(self, content):
        raise NotImplementedError()


class AnnotationResource(ModelResource):
    resource = fields.ForeignKey('aawiki.api.ResourceResource', 'resource')

    class Meta:
        queryset = Annotation.objects.all()
        resource_name = 'annotation'
        authorization= Authorization()
        filtering = {
            "resource": ('exact',)
        }
        serializer = AudacitySerializer()


class ResourceResource(ModelResource):
    annotations = fields.ToManyField('aawiki.api.AnnotationResource', 'annotation_set', null=True, blank=True, full=True)

    class Meta:
        queryset = Resource.objects.all()
        resource_name = 'resource'
        authorization= Authorization()
