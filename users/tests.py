from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/auth/login/', self.credentials, follow=True)
        print(response.context['user'])
        self.assertTrue(response.context['user'].is_active)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        response = self.client.post('/auth/logout/', follow=True)
        print(response.context['user'])
        self.assertFalse(response.context['user'].is_active)
        self.assertFalse(response.context['user'].is_authenticated)



