from django import forms
from django.contrib import admin
from collection.models import Sound
from collection.widgets import AdminAudioWidget


class SoundAdminForm(forms.ModelForm):
    class Meta:
        model = Sound
        widgets = {
            'sound': AdminAudioWidget,
        }


class SoundAdmin(admin.ModelAdmin):
    form = SoundAdminForm


admin.site.register(Sound, SoundAdmin)
