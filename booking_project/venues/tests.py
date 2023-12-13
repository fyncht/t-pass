from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Booking, Venue
import datetime


# Create your tests here.

class VenueTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_venue(self):
        url = reverse('venue-list')
        data = {
            'name': 'Test Venue',
            'description': 'A test venue',
            'address': '123 Test',
            'services': {'sound': 'Good', 'lighting': 'Bright'},
            'availability': {'monday': '09:00-17:00'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venue.objects.count(), 1)
        self.assertEqual(Venue.objects.get().name, 'Test Venue')


class BookingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.venue = Venue.objects.create(
            name='Test Venue 5',
            description='A test venue',
            address='123 Test Street',
            services={'sound': 'Good', 'lighting': 'Bright'},
            availability={'wednesday': '06:00-23:59'}
        )

    def test_create_booking(self):
        url = reverse('booking-list')
        data = {
            'venue': self.venue.id,
            'start_time': datetime.datetime.now(),
            'end_time': datetime.datetime.now() + datetime.timedelta(hours=2),
            'user_contact': 'user1@example.com'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().user_contact, 'user1@example.com')
