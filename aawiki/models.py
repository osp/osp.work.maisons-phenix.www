from django.db import models
from django.core.urlresolvers import reverse


class Resource(models.Model):
    """Represents a resource such as a web video or audio file"""
    url = models.URLField(verify_exists=False, max_length=255)
    
    def __unicode__(self):
        return self.url
    
    def get_absolute_url(self):
        return reverse('resource-detail', kwargs={'pk': self.pk})


class Annotation(models.Model):
    """Represent an annotation"""
    resource = models.ForeignKey(Resource)
    top = models.IntegerField(default=10)
    left = models.IntegerField(default=10)
    width = models.IntegerField(default=300)
    height = models.IntegerField(default=400)
    body = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.body[0:100]
