from app.models import EventLog
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password


# Create your views here.

#add user view
def create_user(request, username, password):
    data = {
        'username': username
    }
    User.objects.update_or_create(**data)
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    return JsonResponse('account created successfully', safe=False)

def create_superuser(request, username, password):
    data = {
        'username': username
    }
    User.objects.create_superuser(**data)
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    return JsonResponse('account created successfully', safe=False)

#delete user
def delete_user(request, username, password):
    user = User.objects.get(username=username)
    passes = check_password(password, user.password)
    if passes is True:
        User.objects.filter(id=user.id).delete()
        return JsonResponse('User deleted successfully', safe=False)
    else:
        return JsonResponse("User credentials not correct", safe=False)

#get all usernames
def list_all_users(request, username, password):
    try:
        user = User.objects.get(username=username)
        passes = check_password(password, user.password)
        if passes is True:
            data = User.objects.all().values('username', 'is_superuser')
            response = []
            for a_user in data:
                response.append(a_user)
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse("User credentials not correct", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse("User does not exist", safe = False)

#check if user exists
def login(request, username, password, **kwargs):
    try:
        user = User.objects.get(username=username)
        passes = check_password(password, user.password)
        if passes is True:
            return JsonResponse("User logged in successfully", safe=False)
        else:
            return JsonResponse("User credentials not correct", safe = False)
    except ObjectDoesNotExist:
        return JsonResponse("User does not exist", safe = False)


#view to recieve and store events
def log_event(request, username, password, event_id, event_type, event_data, *args, **kwargs):
    data = {
        'event_id': event_id,
        'event_type': event_type,
        'event_data': event_data,
        'performed_by': username
    }
    try:
        user = User.objects.get(username=username)
        passes = check_password(password, user.password)
        if passes is True:
            EventLog.objects.update_or_create(**data)
            return JsonResponse('event logged successfully', safe=False)
        else:
            return JsonResponse("User credentials not correct", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse("User does not exist", safe=False)


#view to retrieve events
def retrieve_all_events(request, username, password):
    data = EventLog.objects.all().values()
    response = []
    for event in data:
        response.append(event)
    try:
        user = User.objects.get(username=username)
        passes = check_password(password, user.password)
        if passes is True:
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse("User credentials not correct", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse("User does not exist", safe=False)


#view to return event by id
def retrieve_event_by_id(request,username, password, event_id, *args, **kwaargs):
    data = EventLog.objects.filter(event_id=event_id).values()
    try:
        user = User.objects.get(username=username)
        passes = check_password(password, user.password)
        try:
            if passes is True:
                return JsonResponse(data[0], safe=False)
            else:
                return JsonResponse("User credentials not correct", safe=False)
        except IndexError:
            return JsonResponse(f"Event with event_id {event_id} does not exist", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse("User doest not exist", safe=False)

def delete_event(request,username, password, event_id, *args, **kwaargs):
    try:
        user = User.objects.get(username=username)
        data = EventLog.objects.get(event_id=event_id)
        passes = check_password(password, user.password)
        if passes is True:
            data.delete()
            return JsonResponse("Event deleted successfully", safe=False)
        else:
            return JsonResponse("User credentials not correct", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(f"Event with event_id {event_id} does not exist", safe=False)

def hard_delete_event(request,username, password, event_id, *args, **kwaargs):
    try:
        user = User.objects.get(username=username)
        data = EventLog.objects.get(event_id=event_id)
        passes = check_password(password, user.password)
        if passes is True:
            data.hard_delete()
            return JsonResponse("Event deleted successfully", safe=False)
        else:
            return JsonResponse("User credentials not correct", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(f"Event with event_id {event_id} does not exist", safe=False)

def delete_all_events(request,username, password, **kwaargs):
    try:
        user = User.objects.get(username=username)
        data = EventLog.objects.all()
        passes = check_password(password, user.password)
        if passes is True:
            data.delete()
            return JsonResponse("Events deleted successfully", safe=False)
        else:
            return JsonResponse("User credentials not correct", safe=False)
    except ObjectDoesNotExist:
        return JsonResponse(f"User does not exist", safe=False)

#Handling eceptions globallly
def page_not_found_view(request, exception):
    return JsonResponse("Requested url does not exist", safe=False)

def custom_error_view(request, exception=None):
    return JsonResponse("500 server error", safe=False)