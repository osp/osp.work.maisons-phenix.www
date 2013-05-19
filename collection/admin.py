from django.contrib import admin
from collection.models import Category, Completude, Nature, Sound, Relationship


class RelationshipInline(admin.TabularInline):
    model = Sound.tags.through


class SoundAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline,]


admin.site.register(Category)
admin.site.register(Completude)
admin.site.register(Nature)
admin.site.register(Sound, SoundAdmin)
