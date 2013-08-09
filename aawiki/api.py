from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from aawiki.models import Annotation, Resource


class AnnotationResource(ModelResource):
    resource = fields.ForeignKey('aawiki.api.ResourceResource', 'resource')

    class Meta:
        queryset = Annotation.objects.all()
        resource_name = 'annotation'
        authorization= Authorization()


class ResourceResource(ModelResource):
    annotations = fields.ToManyField('aawiki.api.AnnotationResource', 'annotation_set', null=True, blank=True, full=True)

    class Meta:
        queryset = Resource.objects.all()
        resource_name = 'resource'
        authorization= Authorization()
