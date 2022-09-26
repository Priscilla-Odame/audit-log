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
from app.views import log_event, retrieve_all_events, retrieve_event_by_id

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logevent/<str:event_id>/<str:event_type>/<str:event_data>', log_event, name='logevent'),
    path('event/<str:event_id>', retrieve_event_by_id, name='get_event_by_id'),
    path('event', retrieve_all_events, name='get_all_events')
]
