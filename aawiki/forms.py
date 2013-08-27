from django import forms
from aawiki.models import Annotation


class AnnotationUpdateForm(forms.ModelForm):
    class Meta:
        model = Annotation
        exclude = ('width', 'height', 'left', 'top')
