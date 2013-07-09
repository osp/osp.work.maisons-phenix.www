import markdown
from django.db import models
from django.conf import settings
from collection.tasks import transcode, ffmpeg2theora, ffmpeg2vp8, wav2spectrogram, githash, get_sound_duration
import widgets
import os
from aacore.sniffers import AAResource


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

    @property
    def spectrogram_path(self):
        fn = '%s.png' % githash(self.sound.path)
        return os.path.join(settings.MEDIA_ROOT, 'spectrograms', fn)

    @property
    def spectrogram_url(self):
        fn = '%s.png' % githash(self.sound.path)
        return os.path.join(settings.MEDIA_URL, 'spectrograms', fn)

    def save(self, *args, **kwargs):
        super(Sound, self).save(*args, **kwargs)

        try:
            duration = int(get_sound_duration(self.sound.path)) * 4
            if duration < 11:
                duration = 11
            wav2spectrogram(self.sound.path, width=duration)
        except RuntimeError:
            pass

        # indexes the page in the RDF store
        #path = reverse('aawiki:page-detail', kwargs={'slug': slug})
        #url = '%s://%s%s' % (request.is_secure() and 'https' or 'http', request.get_host(), self.get_absolute_url())
        url = 'http://localhost:8000%s' % self.get_absolute_url()
        AAResource(url).index()

        url = 'http://localhost:8000%s' % self.sound.url
        AAResource(url).index()

        #transcode.delay(self.sound.path)
        #ffmpeg2theora.delay(self.sound.path)
        #ffmpeg2vp8.delay(self.sound.path)
