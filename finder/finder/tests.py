from django.test import TestCase
from finder.models import Event, EventType, CovidSafetyLevel
from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime

# Create your tests here.
class EventTestCase(TestCase):
    def setUp(self):
        protest = EventType.objects.get( eventtype = "Protest" )
        Event.objects.create(
            name = "e1",
            description = "a test description",
            address = "2111 Jefferson Park Ave., Charlottesville, VA 22903",
            eventtype = protest,
            startdate = timezone.now(),
            remote = False,
            size = 12,
            outdoor = False,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e2",
            description = "a test description",
            address = "2111 JPA",
            eventtype = protest,
            startdate = timezone.now(),
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e3",
            description = "a test description",
            address = "2111 JPA",
            eventtype = EventType.objects.get( eventtype = "Academic Seminar" ),
            startdate = timezone.now(),
            remote = False,
            size = 5,
            outdoor = True,
            masks = True,
            distanced = True,
        )

        Event.objects.create(
            name = "e4",
            description = "a test description",
            address = "2111 JPA",
            eventtype = EventType.objects.get( eventtype = "Concert" ),
            startdate = timezone.now(),
            remote = False,
            size = 5,
            outdoor = True,
            masks = True,
            distanced = True,
        )

        Event.objects.create(
            name = "e5",
            description = "a test description",
            address = "2111 Jefferson Park Ave., Charlottesville, VA 22903",
            eventtype = protest,
            startdate = timezone.now(),
            remote = False,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

    def test_lat_long_exists(self):
        event = Event.objects.get(name = "e1")
        self.assertNotEqual(event.latitude, 0)
        self.assertNotEqual(event.longitude, 0)

    def test_lat_long_correct(self):
        event = Event.objects.get(name = "e1")
        self.assertEqual(event.latitude, 38.0263463)
        self.assertEqual(event.longitude, -78.51441439999999)

    def test_no_safety(self):
        event = Event.objects.get(name = "e1")
        self.assertEqual(event.covidsafetylevel.covidsafetylevel, '0')

    def test_low_safety(self):
        event = Event.objects.get(name = "e5")
        self.assertEqual(event.covidsafetylevel.covidsafetylevel, '1')

    def test_full_safety_remote(self):
        event = Event.objects.get(name = "e2")
        self.assertEqual(event.covidsafetylevel.covidsafetylevel, '5')
    
    def test_full_safety_not_remote(self):
        event = Event.objects.get(name = "e3")
        self.assertEqual(event.covidsafetylevel.covidsafetylevel, '5')

    def test_some_safety(self):
        event = Event.objects.get(name = "e4")
        self.assertEqual(event.covidsafetylevel.covidsafetylevel, '4')

class SearchCovidEventTestCase(TestCase):
    def setUp(self):
        event_type = EventType.objects.get( eventtype = "Protest" )
        Event.objects.create(
            name = "e1",
            description = "e1 description",
            address = "2111 JPA",
            eventtype = event_type,
            startdate = timezone.now(),
            remote = False,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e2",
            description = "e2 description",
            address = "2111 JPA",
            eventtype = event_type,
            startdate = timezone.now(),
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

    def test_ok_response(self):
        response = self.client.get(reverse('finder:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_high_safety(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 5, 'eventtype':'all'})
        for event in response.context['events_list']:
            self.assertEqual(event.covidsafetylevel.covidsafetylevel, '5')

    def test_search_low_safety(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 0, 'eventtype':'all'})
        for event in response.context['events_list']:
            self.assertGreaterEqual(event.covidsafetylevel.covidsafetylevel, '0')

class SearchTypeEventTestCase(TestCase):
    def setUp(self):
        protest = EventType.objects.get( eventtype = "Protest" )
        Event.objects.create(
            name = "e1",
            description = "e1 description",
            address = "2111 JPA",
            eventtype = EventType.objects.get( eventtype = "Party" ),
            startdate = timezone.now(),
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e2",
            description = "e2 description",
            address = "2111 JPA",
            eventtype = protest,
            startdate = timezone.now(),
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e3",
            description = "e2 description",
            address = "2111 JPA",
            eventtype = protest,
            startdate = timezone.now(),
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )
    
    def test_search_party(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 1, 'eventtype':'Party'})
        for event in response.context['events_list']:
            self.assertEqual(event.eventtype.eventtype, 'Party')

    def test_search_protest(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 1, 'eventtype':'Protest'})
        for event in response.context['events_list']:
            self.assertEqual(event.eventtype.eventtype, 'Protest')

class SearchDateEventTestCase(TestCase):
    def setUp(self):
        party = EventType.objects.get( eventtype = "Party" )
        Event.objects.create(
            name = "e1",
            description = "e1 description",
            address = "2111 JPA",
            eventtype = party,
            startdate = '2020-11-27 13:00',
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e2",
            description = "e2 description",
            address = "2111 JPA",
            eventtype = party,
            startdate = '2020-11-28 13:00',
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e3",
            description = "e2 description",
            address = "2111 JPA",
            eventtype = party,
            startdate = '2020-11-29 13:00',
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )
    
    def test_search_on_date(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 1, 'eventtype': 'Party', 'date1': '2020-11-27', 'dateopt': 'on'})
        for event in response.context['events_list']:
            self.assertEqual(event.startdate.date(), datetime.date(2020, 11, 27))

    def test_search_after_date(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 1, 'eventtype': 'Party', 'date1': '2020-11-27', 'dateopt': 'after'})
        for event in response.context['events_list']:
            self.assertGreaterEqual(event.startdate.date(), datetime.date(2020, 11, 27))

    def test_search_before_date(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 1, 'eventtype': 'Party', 'date1': '2020-11-28', 'dateopt': 'before'})
        for event in response.context['events_list']:
            self.assertLessEqual(event.startdate.date(), datetime.date(2020, 11, 28))

    def test_search_between_date(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 1, 'eventtype': 'Party', 'date1': '2020-11-27', 'date2': '2020-11-27', 'dateopt': 'between'})
        for event in response.context['events_list']:
            self.assertLessEqual(event.startdate.date(), datetime.date(2020, 11, 27))
            self.assertGreaterEqual(event.startdate.date(), datetime.date(2020, 11, 27))

class SearchMultipleEventTestCase(TestCase):
    def setUp(self):
        party = EventType.objects.get( eventtype = "Party" )
        concert = EventType.objects.get( eventtype = "Concert" )
        Event.objects.create(
            name = "e1",
            description = "e1 description",
            address = "2111 JPA",
            eventtype = party,
            startdate = '2020-11-27 13:00',
            remote = True,
            size = 12,
            outdoor = True,
            masks = False,
            distanced = False,
        )

        Event.objects.create(
            name = "e2",
            description = "e2 description",
            address = "2111 JPA",
            eventtype = concert,
            startdate = '2020-11-28 13:00',
            remote = False,
            size = 100,
            outdoor = True,
            masks = True,
            distanced = False,
        )
    
    def test_search_multiple_1(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 5, 'eventtype': 'Party', 'date1': '2020-11-27', 'dateopt': 'on'})
        for event in response.context['events_list']:
            self.assertEqual(event.covidsafetylevel.covidsafetylevel, '5')
            self.assertEqual(event.startdate.date(), datetime.date(2020, 11, 27))
            self.assertEqual(event.eventtype.eventtype, 'Party')

    def test_search_multiple_2(self):
        response = self.client.post(reverse('finder:search'), {'covidsafetylevel': 2, 'eventtype': 'Concert', 'date1': '2020-11-27', 'dateopt': 'after'})
        for event in response.context['events_list']:
            self.assertGreaterEqual(event.covidsafetylevel.covidsafetylevel, '2')
            self.assertGreaterEqual(event.startdate.date(), datetime.date(2020, 11, 27))
            self.assertEqual(event.eventtype.eventtype, 'Concert')

class UrlTestCase(TestCase):
    def test_redirect_after_reg(self):
        response = self.client.post(reverse('finder:reg_event', kwargs={'id': 0}), {'fname': 'sonali', 'lname': 'luthar', 'email': 'sl2ae@virginia.edu'})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(reverse('finder:logout'))
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        response = self.client.get(reverse('finder:add_event'))
        self.assertEqual(response.status_code, 200)

    def test_event_list(self):
        response = self.client.get(reverse('finder:event_list'))
        self.assertEqual(response.status_code, 200)

    def test_events(self):
        response = self.client.get(reverse('finder:eventlist'))
        self.assertEqual(response.status_code, 200)