from django.contrib import admin
from aawiki.models import Annotation, Resource


class AnnotationAdmin(admin.ModelAdmin):
    pass


class ResourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Resource, ResourceAdmin)
