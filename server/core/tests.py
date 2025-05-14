from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import *


class VenueTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testvenue',
            password='testpass123',
            email='test@example.com'
        )
        self.venue = Venue.objects.create(
            user=self.user,
            name='Test Club',
            city='Test City',
            phone='+79123456789'
        )
        self.client = APIClient()

    def test_venue_registration(self):
        url = reverse('register')
        data = {
            'username': 'newvenue',
            'password': 'newpass123',
            'email': 'new@example.com',
            'name': 'New Club',
            'city': 'New City',
            'phone': '+79123456789'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newvenue').exists())
        self.assertTrue(Venue.objects.filter(name='New Club').exists())

    def test_venue_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Club')


class TrackTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.venue = Venue.objects.create(
            user=self.user,
            name='Test Venue',
            city='Test City',
            phone='+79123456789'
        )
        self.genre = Genre.objects.create(name='Test Genre')
        self.track = Track.objects.create(
            venue=self.venue,
            genre=self.genre,
            title='Test Track',
            artist='Test Artist',
            price=100
        )
        self.client.force_authenticate(user=self.user)

    def test_create_track(self):
        url = reverse('tracks-list', kwargs={'venue_id': self.venue.id})
        data = {
            'genre': self.genre.id,
            'title': 'New Track',
            'artist': 'New Artist',
            'price': 150
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 2)

    def test_get_tracks_list(self):
        url = reverse('tracks-list', kwargs={'venue_id': self.venue.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TrackRequestTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.venue = Venue.objects.create(
            user=self.user,
            name='Test Venue',
            city='Test City',
            phone='+79123456789'
        )
        self.genre = Genre.objects.create(name='Test Genre')
        self.track = Track.objects.create(
            venue=self.venue,
            genre=self.genre,
            title='Test Track',
            artist='Test Artist',
            price=100
        )
        self.client.force_authenticate(user=self.user)

    def test_create_track_request(self):
        url = reverse('track-request-create', kwargs={'venue_id': self.venue.id})
        data = {'track': self.track.id, 'user_fee': 150}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrackRequest.objects.count(), 1)

    def test_min_fee_validation(self):
        url = reverse('track-request-create', kwargs={'venue_id': self.venue.id})
        data = {'track': self.track.id, 'user_fee': 50}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WithdrawalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.venue = Venue.objects.create(
            user=self.user,
            name='Test Venue',
            city='Test City',
            phone='+79123456789',
            balance=1000
        )
        self.client.force_authenticate(user=self.user)

    def test_create_withdrawal(self):
        url = reverse('withdrawal-create')
        data = {
            'amount': 500,
            'account_details': 'Test Account'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WithdrawalRequest.objects.count(), 1)

    def test_insufficient_balance(self):
        url = reverse('withdrawal-create')
        data = {
            'amount': 1500,
            'account_details': 'Test Account'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)