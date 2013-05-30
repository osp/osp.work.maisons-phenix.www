from django.shortcuts import render, redirect
from django.http import HttpResponse
from collection.models import Sound
from collection.tasks import transcode


def sound_list(request):
    return render(request, 'collection/sound_list.html', {"obj_list": Sound.objects.all()})


def points(request):
    return render(request, 'collection/points.html', {"obj_list": Sound.objects.all()})


def convert(request, id):
    sound = Sound.objects.get(id=id)
    task = transcode.delay(sound.sound.path)
    #return redirect('celery-task_status', task_id=task.id)
    return HttpResponse(task.id, mimetype="text/plain")
