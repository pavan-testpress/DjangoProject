from django.test import TestCase
from django.shortcuts import reverse

from exam import fixture


class AuthenticationTestCase(TestCase):

    @fixture
    def user(self):
        user = {
            'first_name': 'Pavan Kumar',
            'last_name': 'Kuppala',
            'username': 'pavankumar',
            'email': 'pavancse17@gmail.com',
            'password1': '143Pavan..',
            'password2': '143Pavan..',

        }
        return user

    def test_get_login_page(self):
        """
        Test to get login page.
        """
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_try_to_login_with_invalid_credentials(self):
        """
        Test to login with invalid credentials
        """
        self.client.post(reverse('authentication:signup'), self.user)
        response = self.client.post(reverse('authentication:login'), {'username': 'dsfsdfs', 'password': '1sfsdf'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/invalidlogin.html')

    def test_post_login_page(self):
        """
        Test to login existing user.
        """
        signup = self.client.post(reverse('authentication:signup'), self.user)
        self.client.get(reverse('authentication:activate',
                                kwargs={'uidb64': signup.context['uid'], 'token': signup.context['token']}))
        response = self.client.post(reverse('authentication:login'), {'username': 'pavankumar', 'password': '143Pavan..'})
        self.assertRedirects(response, reverse('authentication:index'))

    def test_logout_page(self):
        """
        Test to check successful logout functionality.
        """
        response = self.client.get(reverse('authentication:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:login'))
