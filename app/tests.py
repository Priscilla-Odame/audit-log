import json
from django.test import TestCase

from app.models import EventLog
from django.utils import timezone
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# Create your tests here.
class EventlogTestModel(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = 'testuser',
            password = 'testpassword'
        )
        EventLog.objects.create(
            id = 1,
            event_id = 'event1',
            event_type = 'error',
            timestamp = timezone.now(),
            event_data = 'Deleting a customer',
            performed_by = 'testuser'
        )
        EventLog.objects.create(
            id = 2,
            event_id = 'event2',
            event_type = 'log',
            timestamp = timezone.now(),
            event_data = 'Adding a customer',
            performed_by = 'testuser'

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
        response = self.client.get("/event/testuser/testpassword/event1")
        data = json.loads(response.content)
        self.assertEqual(data['event_type'], "error")
    
    def test_log_event(self):
        """
        Testing logging an event
        """
        event = EventLog.objects.get(id=1)
        event.hard_delete()
        response = self.client.post("/logevent/testuser/testpassword/event1/error/testing endpoint")
        data = json.loads(response.content)
        self.assertEqual(data, "event logged successfully")
    
    def test_all_events(self):
        """
        Testing getting all events
        """
        response = self.client.get("/event/testuser/testpassword")
        data = json.loads(response.content)
        event1 = data[0]
        event2 = data[1]
        self.assertEqual(event1['event_type'], "error")
        self.assertEqual(event2['event_type'], "log")

    def test_delete_event(self):
        """
        Testing deleting an event
        """
        response = self.client.delete("/deleteevent/testuser/testpassword/event1")
        data = json.loads(response.content)
        self.assertEqual(data, "Event deleted successfully")