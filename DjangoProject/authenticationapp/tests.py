from django.test import TestCase
from django.shortcuts import reverse

from authenticationapp.models import MyUser


class AuthenticationTestCase(TestCase):
    def setUp(self):
        """
        Create new user for every testcase.
        """
        self.credentials = {
            'username': 'pavan',
            'password': 'pavankumar'
        }
        MyUser.objects.create_user(**self.credentials)

    def test_signup_page(self):
        """
        Test to get signup page.
        """
        response = self.client.get(reverse('authenticationapp:signup'))
        self.assertEqual(response.status_code, 200)

    def test_post_signup_page(self):
        """
        Test to create user through signup page.
        """
        data = {
            'email': "kumar@gmail.com",
            'password1': "pavankumar",
            'password2': "pavankumar"
        }
        response = self.client.post(reverse('authenticationapp:signup'), data)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def test_get_login_page(self):
        """
        Test to get login page.
        """
        response = self.client.get(reverse('authenticationapp:login'))
        self.assertEqual(response.status_code, 200)

    def test_post_login_page(self):
        """
        Test to login existing user.
        """
        response = self.client.post(reverse('authenticationapp:login'), self.credentials)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def test_logout_page(self):
        """
        Test to check successful logout functionality.
        """
        response = self.client.get(reverse('authenticationapp:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authenticationapp:login'))
