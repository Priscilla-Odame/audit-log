"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import (log_event, retrieve_all_events, retrieve_event_by_id, login,
                        delete_event, delete_all_events, hard_delete_event,
                        create_user, create_superuser, list_all_users, delete_user)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adduser/<str:username>/<str:password>', create_user , name='addaccount'),
    path('addadmin/<str:username>/<str:password>', create_superuser , name='addadmin'),
    path('login/<str:username>/<str:password>', login, name='login'),
    path('users/<str:username>/<str:password>', list_all_users , name='listusers'),
    path('deleteuser/<str:username>/<str:password>', delete_user , name='deleteuser'),
    path('logevent/<str:username>/<str:password>/<str:event_id>/<str:event_type>/<str:event_data>', log_event, name='logevent'),
    path('event/<str:username>/<str:password>/<str:event_id>', retrieve_event_by_id, name='get_event_by_id'),
    path('deleteevent/<str:username>/<str:password>/<event_id>', delete_event, name='delete_event'),
    path('deleteevent/<str:username>/<str:password>', delete_all_events, name='delete_all_event'),
    path('harddeleteevent/<str:username>/<str:password>', hard_delete_event, name='hard_delete_event'),
    path('event/<str:username>/<str:password>', retrieve_all_events, name='retrieve_all_events')
]
