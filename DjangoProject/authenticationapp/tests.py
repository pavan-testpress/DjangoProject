from django.test import TestCase
from django.shortcuts import reverse

from authenticationapp.models import MyUser


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'pavan',
            'password': 'pavankumar'
        }
        MyUser.objects.create_user(**self.credentials)

    def testSignupPage(self):
        response = self.client.get(reverse('authenticationapp:signup'))
        self.assertEqual(response.status_code, 200)

    def testPostSignupPage(self):
        data = {
            'email': "kumar@gmail.com",
            'password1': "pavankumar",
            'password2': "pavankumar"
        }
        response = self.client.post(reverse('authenticationapp:signup'), data)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def testGetLoginPage(self):
        response = self.client.get(reverse('authenticationapp:login'))
        self.assertEqual(response.status_code, 200)

    def testPostLoginPage(self):
        response = self.client.post(reverse('authenticationapp:login'), self.credentials)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def testLogoutPage(self):
        response = self.client.get(reverse('authenticationapp:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authenticationapp:login'))
