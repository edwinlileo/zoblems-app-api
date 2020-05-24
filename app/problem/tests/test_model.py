from django.test import TestCase
from django.contrib.auth import get_user_model

from problem import models


def sample_user(email='test@test.com', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ResponseModelTests(TestCase):

    def test_response_str(self):
        """Test the response string representation"""
        response = models.Response.objects.create(
            user=sample_user(),
            description='Sample description'
        )

        self.assertEqual(str(response), response.description)
