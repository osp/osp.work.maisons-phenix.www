import rdflib
import markdown

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

from aawiki.models import Resource, Annotation
from aawiki.forms import AnnotationUpdateForm


class ResourceListView(ListView):
    model = Resource


class ResourceDetailView(DetailView):
    model = Resource


class AnnotationUpdateView(UpdateView):
    model = Annotation
    form_class = AnnotationUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('annotation-update-success')


class AnnotationUpdateSuccessView(TemplateView):
    template_name = "aawiki/annotation_update_success.html"


class ResourceDetailAsRDFView(DetailView):
    model = Resource

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        source = u"\n\n".join([resource.body for resource in self.object.annotation_set.all()])
        md = markdown.Markdown(output_format="xhtml5", extensions=['semanticdata', 'semanticwikilinks'])
        body = md.convert(source)
        rendered = render(request, 'aawiki/rdfa.html', {'body': body})
        graph = rdflib.Graph()
        graph.parse(data=rendered.content,
                source='http://localhost:8000{0}'.format(self.object.get_absolute_url()), 
                format="rdfa")
        turtle = graph.serialize(format='turtle')

        return HttpResponse(turtle, content_type='text/turtle')
