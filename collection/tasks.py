from celery import task
import subprocess
import os.path
import hashlib
try: import simplejson as json
except ImportError: import json


def sha1(path):
    return hashlib.sha1(path).hexdigest()


@task()
def add(x, y):
    return x + y


def get_codec_types(path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", path]
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    (stdout_data, stderr_data) = p1.communicate()
    codec_types = []
    data = json.loads(stdout_data)
    for stream in data['streams']:
        codec_types.append(stream['codec_type'])

    return codec_types


@task()
def transcode(path):
    codec_types = get_codec_types(path)

    type = "video" if "video" in codec_types else "audio"

    if type is "video":
        ext = ".ogv"
    else:
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
    print(fn)

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
