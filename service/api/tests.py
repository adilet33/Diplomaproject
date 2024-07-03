from django.test import TestCase

# myapp/tests.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User

class UserTests(APITestCase):

    def test_register(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        self.test_register()
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

