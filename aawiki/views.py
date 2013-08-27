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
