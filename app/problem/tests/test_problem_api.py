from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from problem.models import Problem, Response
from problem.serializers import ProblemSerializer


PROBLEMS_URL = reverse('problem:problem-list')


def sample_response(user, description='Sample description'):
    """Creates a sample response"""
    return Response.objects.create(user=user, description=description)


class PublicProblemsApiTests(TestCase):
    """Test the publicly avaiable problem API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(PROBLEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProblemApiTests(TestCase):
    """Test the privatly avaiable problem API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_problem_list(self):
        """Test retriving a list of problems"""
        Problem.objects.create(user=self.user, title='sample title 1')
        Problem.objects.create(user=self.user, title='sample title 2')

        res = self.client.get(PROBLEMS_URL)

        problems = Problem.objects.all().order_by('title')
        serializer = ProblemSerializer(problems, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_problem_base_success(self):
        """Test create a problem with valid payload is successful"""
        payload = {'title': 'Sample title 1'}
        self.client.post(PROBLEMS_URL, payload)

        exists = Problem.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_problem_base_invalid(self):
        """Test creating invalid problem fails"""
        payload = {'title': ''}
        res = self.client.post(PROBLEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_problem_with_responses(self):
        """Test creating problem with responses"""
        response1 = sample_response(user=self.user, description='Sample des 1')
        response2 = sample_response(user=self.user, description='Sample des 2')
        payload = {'title': 'Sample title', 'responses': [response1.id, \
                                                          response2.id]}
        res = self.client.post(PROBLEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        problem = Problem.objects.get(id=res.data['id'])
        responses = problem.responses.all()
        self.assertEqual(responses.count(), 2)
        self.assertIn(response1, responses)
        self.assertIn(response2, responses)

    def test_create_problem_with_accessUsers(self):
        """Test creating problem with accessUsers"""
        user1 = get_user_model().objects.create_user('test@test1.com', \
                                                     'test1pass123')
        user2 = get_user_model().objects.create_user('test@test2.com', \
                                                     'test2pass123')
        payload = {'title': 'Sample title', 'accessUsers': [user1.id, \
                                                            user2.id]}
        res = self.client.post(PROBLEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        problem = Problem.objects.get(id=res.data['id'])
        accessUsers = problem.accessUsers.all()
        self.assertEqual(accessUsers.count(), 2)
        self.assertIn(user1, accessUsers)
        self.assertIn(user2, accessUsers)
