from django.shortcuts import render, redirect
from django.http import HttpResponse
from collection.models import Sound
from collection.tasks import add, transcode


def sound_list(request):
    add.delay(1, 2)
    return render(request, 'collection/sound_list.html', {"obj_list": Sound.objects.all()})


def convert(request, id):
    sound = Sound.objects.get(id=id)
    task = transcode.delay(sound.sound.path)
    #return redirect('celery-task_status', task_id=task.id)
    return HttpResponse(task.id, mimetype="text/plain")