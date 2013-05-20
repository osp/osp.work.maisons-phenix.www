import sys
import markdown
from django.db import models
from django.conf import settings
from collection.tasks import transcode, ffmpeg2theora, ffmpeg2vp8
import widgets 


sys.path.append('/usr/lib/python2.7/site-packages/')
import RDF


#options = "hash-type='bdb', contexts='yes', dir='%s'" % settings.RDF_STORAGE_DIR
#storage = RDF.HashStorage(settings.RDF_STORAGE_NAME, options=options)
#RDF_MODEL = RDF.Model(storage)


class Sound(models.Model):
    sound = models.FileField(upload_to="sound")
    name = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('sound-detail', (), {'pk': str(self.pk)})

    @property
    def html(self):
        md = markdown.Markdown(output_format="html5", extensions=['semanticdata'])
        return md.convert(self.body)

    def save(self, *args, **kwargs):
        super(Sound, self).save(*args, **kwargs)
        url = self.sound.url

        #transcode.delay(self.sound.path)
        #ffmpeg2theora.delay(self.sound.path)
        #ffmpeg2vp8.delay(self.sound.path)
