from django import forms
from django.utils.safestring import mark_safe


class AdminAudioWidget(forms.FileInput):
    """
    A AudioField Widget for admin that shows an audio tag.
    """

    def __init__(self, attrs={}):
        super(AdminAudioWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        output.append(super(AdminAudioWidget, self).render(name, value, attrs))
        if value and hasattr(value, "url"):
            output.append('<audio src="%s" controls></audio>' % value.url)
        return mark_safe(u''.join(output))
