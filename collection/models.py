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


class Sound(models.Model):
    sound = models.FileField(upload_to="sound")
    completude = models.ForeignKey(Completude)
    short_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    nature = models.ForeignKey(Nature)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Sound, self).save(*args, **kwargs)
        transcode.delay(self.sound.path)
        #ffmpeg2theora.delay(self.sound.path)
        #ffmpeg2vp8.delay(self.sound.path)
