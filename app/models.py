from django.db import models

# Create your models here.
class EventLog(models.Model):
    event_id = models.CharField(max_length=300, unique=True)
    event_type = models.CharField(max_length=600)
    timestamp = models.DateTimeField(auto_now=True)
    event_data = models.JSONField(default = dict)
