from django.shortcuts import render
from .models import ScheduleVisit
from django.db.models import Max


def schedule_view(request):
    latest_revision = ScheduleVisit.objects.aggregate(Max('revision'))['revision__max']
    latest_visits = ScheduleVisit.objects.all()
    context = {
        'latest_visits': latest_visits,
        'max_revision': latest_revision or 'No visits found.'
    }
    return render(request, 'schedule.html', context)