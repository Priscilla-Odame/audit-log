from app.models import EventLog
from django.http import JsonResponse
from django.http import HttpResponse


# Create your views here.

#view to recieve and store events
def log_event(request, event_id, event_type, event_data, *args, **kwargs):
    data = {
        'event_id': event_id,
        'event_type': event_type,
        'event_data': event_data
    }
    EventLog.objects.update_or_create(**data)
    return HttpResponse(status = 200)


#view to retrieve events
def retrieve_all_events(request):
    data = EventLog.objects.all().values()
    response = []
    for event in data:
        response.append(event)

    return JsonResponse(response, safe=False)


#view to return event by id
def retrieve_event_by_id(request,event_id, *args, **kwaargs):
    data = EventLog.objects.filter(event_id=event_id).values()

    return JsonResponse(data[0], safe=False)
