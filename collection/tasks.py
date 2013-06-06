from celery import task
import subprocess
import os.path
import hashlib
try: import simplejson as json
except ImportError: import json
from django.conf import settings
import svt


def get_sound_duration(fname):
    import wave
    import contextlib
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def sha1(path):
    return hashlib.sha1(path).hexdigest()


def githash(path, block_size=2**20):
    """ 
    Returns an sha1 hash based on the content of a file.

    Should produce the same SHA1 hash git uses for a particular file.
    """
    s = hashlib.sha1()

    filesize = os.path.getsize(path)
    s.update("blob %u\0" % filesize)

    f = open(path, "rb")

    while True:
        data = f.read(block_size)
        if not data:
            break
        s.update(data)

    return s.hexdigest()


# Adapted from http://blog.will-daly.com/2012/11/22/using-ffprobe-to-validate-video-content/
class FFProbe:
    """Wrapper for the ffprobe command"""

    def get_streams_dict(self, url):
        """ Returns a Python dictionary containing
        information on the audio/video streams contained
        in the file located at 'url'

        If no stream information is available (e.g.
        because the file is not a video), returns
        an empty dictionary"""
        command = self._ffprobe_command(url)
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, err = process.communicate()
        return json.loads(output)

    def _ffprobe_command(self, url):
        return ['ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                str(url)]


def get_stream_types(url):
    """ Use ffprobe wrapper to check whether the file
    at url is a valid video file """
    ffprobe = FFProbe()

    # Attempt to get the stream dictionary
    # If any error occurs, assume the file not a video
    try:
        streamDict = ffprobe.get_streams_dict(url)
    except Exception as e:
        return False
    # If there are no streams available,
    # then the file is not a video
    if 'streams' not in streamDict:
        return False
    # A dictionnary holding codec types
    streams = []

    # Check each stream, looking for a video
    for streamInfo in streamDict['streams']:
        # Check if the codec is a video
        codecType = streamInfo['codec_type']

        if codecType == 'video':
            # Images are sometimes parsed as videos,
            # so also check that there's at least
            # 1 second of video
            duration = streamInfo['duration']
            if float(duration) > 1.0:
                # It is a video, appends it
                streams.append('video')

        elif codecType == 'audio':
            streams.append('audio')

    # Returns the collected stream types
    return streams


@task()
def transcode(path):
    stream_types = get_stream_types(path)

    if not stream_types:
        return None

    if 'video' in stream_types:
        type = 'video'
        ext = ".ogv"
    elif 'audio' in stream_types:
        type = 'audio'
        ext = ".oga"

    fn = "/home/aleray/work/osp.work.maisons-phenix.www/phenix/public/media/sound/"
    fn += sha1(path) + ext

    if not os.path.exists(fn):
        subprocess.call(["ffmpeg2theora", "-o", fn, path])

    return {"type": type, "url": sha1(path) + ext}

@task()
def ffmpeg2theora(path):
    codec_types = get_codec_types(path)

    if "video" in codec_types:
        ext = "ogv"
    else:
        ext = "oga"

    fn = sha1(path) + ext

    cmd = ["ffmpeg"]

    if "video" in codec_types:
        cmd.extend([
            #"-vcodec", "libtheora",
            "-vcodec", "theora",
            "-g", "15",
            "-qscale", "6",
        ])

    cmd.extend([
        "-acodec", "libvorbis",
        "-ac", "2",
        "-aq", "3",
        "-i", path,
        fn
    ])

    subprocess.call(cmd)

@task()
def ffmpeg2vp8(path):
    subprocess.call(["ffmpeg", "-i", path, "-vcodec", "libvpx", "bla.webm"])


@task()
def wav2spectrogram(path, width=600):
    fn = '%s.png' % githash(path)

    input_file = path
    output_file_w = ''  # not used as wavefile is set to `0`
    output_file_s = os.path.join(settings.MEDIA_ROOT, 'spectrograms', fn)
    image_width = width
    image_height = 50
    fft_size = 2048
    f_max = 22050
    f_min = 10
    wavefile = 0
    palette = 3
    channel = 1

    args = (input_file, output_file_w, output_file_s, image_width, image_height, fft_size, f_max, f_min, wavefile, palette, channel)

    svt.create_png(*args)
