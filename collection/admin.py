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


def save(modeladmin, request, queryset):
    for obj in queryset:
        obj.save()

save.short_description = "Save selected sounds"


class SoundAdmin(admin.ModelAdmin):
    form = SoundAdminForm
    actions = [save]


admin.site.register(Sound, SoundAdmin)
