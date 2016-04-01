from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

from logger.models import Log

import json

# Create your views here.

def login(request):
    # context = RequestContext(request, {
    #     'request': request, 'user': request.user})
    # return render_to_response('login.html', context_instance=context)

    return render(request, 'login.html')

@login_required(login_url='/')
def dnevnik(request):

    user = request.user

    logs = user.log_set.all()

    context = {}
    context['logs'] = logs

    return render(request, 'dnevnik.html', context)

@csrf_exempt
def addLog(request):
    user = request.user
    date = datetime.strptime(request.POST['date'], '%d.%m.%Y')
    theme = request.POST['theme']
    notes = request.POST['notes']

    if request.POST['is_implicit'] == 'true':
        is_implicit = True
        fallacies = {}
    else:
        is_implicit = False
        fallacies = json.loads(request.POST['fallacies'])

    newlog = Log(user=user, date=date, is_implicit=is_implicit, fallacies=fallacies, theme=theme, notes=notes)
    newlog.save()

    return HttpResponse(1)

@csrf_exempt
def updateLog(request):
    user = request.user
    log = Log.objects.get(pk=int(request.POST['log_id']))
    log.date = datetime.strptime(request.POST['date'], '%d.%m.%Y')
    log.theme = request.POST['theme']
    log.notes = request.POST['notes']

    if request.POST['is_implicit'] == 'true':
        log.is_implicit = True
        log.fallacies = {}
    else:
        log.is_implicit = False
        log.fallacies = json.loads(request.POST['fallacies'])

    log.save()

    return HttpResponse(1)

@csrf_exempt
def deleteLog(request):
    log = Log.objects.get(pk=int(request.POST['log_id']))

    log.delete()

    return HttpResponse(1)

@login_required
def editLog(request, log_id):
    user = request.user
    log = Log.objects.get(pk=int(log_id))

    context = {
        'user': user,
        'log': log
    }

    if log.is_implicit:
        return render(request, 'urediimplicitne.html', context)
    else:
        return render(request, 'uredilogicne.html', context)


@login_required(login_url='/')
def choose(request):

    return render(request, 'choose.html')

@login_required(login_url='/')
def implicitne(request):

    return render(request, 'implicitne.html')

@login_required(login_url='/')
def logicne(request):

    return render(request, 'logicne.html')

@login_required(login_url='/')
def logout(request):
    auth_logout(request)
    return redirect('/')
