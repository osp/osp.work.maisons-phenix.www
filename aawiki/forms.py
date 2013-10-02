from django import forms
from aawiki.models import Annotation
from aawiki.utils.audacity import audacity_to_srt 


class AnnotationUpdateForm(forms.ModelForm):
    class Meta:
        model = Annotation
        exclude = ('width', 'height', 'left', 'top')

    def clean_body(self):
        data = self.cleaned_data['body']
        data = audacity_to_srt(data)

        return data
