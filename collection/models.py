from django.db import models
from collection.tasks import transcode, ffmpeg2theora, ffmpeg2vp8


class Completude(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Nature(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Sound(models.Model):
    sound = models.FileField(upload_to="sound")
    completude = models.ForeignKey(Completude, blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    nature = models.ForeignKey(Nature, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Category, through='Relationship', related_name="foo_set")

    def __unicode__(self):
        return self.name

    #def save(self, *args, **kwargs):
        #super(Sound, self).save(*args, **kwargs)
        #transcode.delay(self.sound.path)
        #ffmpeg2theora.delay(self.sound.path)
        #ffmpeg2vp8.delay(self.sound.path)


class Relationship(models.Model):
    category = models.ForeignKey(Category)
    sound = models.ForeignKey(Sound)
    value = models.CharField(max_length=255)
