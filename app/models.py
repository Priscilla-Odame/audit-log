from django.db import models
from app.soft_delete_model import SoftDeleteModel

# Create your models here.
class EventLog(SoftDeleteModel):
    event_id = models.CharField(max_length=300, unique=True)
    event_type = models.CharField(max_length=600)
    timestamp = models.DateTimeField(auto_now=True)
    event_data = models.JSONField(default = dict)
    performed_by = models.CharField(max_length=300)
