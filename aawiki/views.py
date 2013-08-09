from django.views.generic.detail import DetailView
from aawiki.models import Resource


class ResourceDetailView(DetailView):
    model = Resource
