import json
from django.test import TestCase

from app.models import EventLog
from django.utils import timezone
from rest_framework.test import APIClient

# Create your tests here.
class EventlogTestModel(TestCase):
    def setUp(self):
        EventLog.objects.create(
            id = 1,
            event_id = 'event1',
            event_type = 'error',
            timestamp = timezone.now(),
            event_data = 'Deleting a customer'
        )
        EventLog.objects.create(
            id = 2,
            event_id = 'event2',
            event_type = 'log',
            timestamp = timezone.now(),
            event_data = 'Adding a customer',
        )
        self.client = APIClient()

    def test_event_created(self):
        event1 = EventLog.objects.get(event_id='event1')
        event2 = EventLog.objects.get(event_type = 'log')
        self.assertEqual(event1.event_type, 'error')
        self.assertEqual(event2.event_id, 'event2')

    def test_get_event_by_id(self):
        """
        Testing getting an event by id
        """
        response = self.client.get("/event/event1")
        data = json.loads(response.content)
        self.assertEqual(data['event_type'], "error")
    
    def test_all_events(self):
        """
        Testing getting all events
        """
        response = self.client.get("/event")
        data = json.loads(response.content)
        event1 = data[0]
        event2 = data[1]
        self.assertEqual(event1['event_type'], "error")
        self.assertEqual(event2['event_type'], "log")
