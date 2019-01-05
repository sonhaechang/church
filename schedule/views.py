import os
import calendar
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from schedule.models import Schedule


# Create your views here.
def schedule(request):
    return render(request, 'schedule/schedule.html')


def schedule_ajax(request):
    schedule = Schedule.objects.all()

    data = []

    for i in range(len(schedule)):
        title = schedule[i].title
        start = schedule[i].start
        end = schedule[i].end
        jsondata = {
            'title':title,
            'start':start,
            'end':end,
        }
        data.append(jsondata)
        # data.append(schedule[i].title)
        # data.append(schedule[i].start)
        # data.append(schedule[i].end)

    # print(data)
    return JsonResponse(data, safe=False)
