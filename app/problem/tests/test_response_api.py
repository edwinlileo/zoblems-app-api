from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from problem.models import Response

from problem.serializers import ResponseSerializer


RESPONSE_URL = reverse('problem:response-list')


class PublicResponseTests(TestCase):
    """Test the public avaiable response API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retriving responses"""
        res = self.client.get(RESPONSE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateResponseTests(TestCase):
    """Test the unauthorized user response API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_responses(self):
        """Test retriving responses"""
        Response.objects.create(user=self.user, description='Sample 1')
        Response.objects.create(user=self.user, description='Sample 2')

        res = self.client.get(RESPONSE_URL)

        responses = Response.objects.all().order_by('description')
        serializer = ResponseSerializer(responses, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_response_successful(self):
        """Test creating a new response"""
        payload = {'description': 'Sample description'}
        self.client.post(RESPONSE_URL, payload)

        exists = Response.objects.filter(
            user=self.user,
            description=payload['description']
        ).exists()
        self.assertTrue(exists)

    def test_create_response_invalid(self):
        """Test creating a new response iwth invalid payload"""
        payload = {'description': ''}
        res = self.client.post(RESPONSE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
