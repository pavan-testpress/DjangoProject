from django.test import TestCase
from django.shortcuts import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from exam import fixture

from authentication.models import MyUser


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

    def test_signup_page(self):
        """
        Test to get signup page.
        """
        response = self.client.get(reverse('authentication:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/signup.html')

    def test_post_signup_page(self):
        """
        Test to create user through signup page.
        """
        response = self.client.post(reverse('authentication:signup'), self.user)
        self.assertEqual(response.context['domain'], 'testserver')
        self.assertEqual(response.context['uid'],
                         urlsafe_base64_encode(force_bytes(response.context['user'].pk)).decode())

    def test_try_to_login_before_verification(self):
        self.client.post(reverse('authentication:signup'), self.user)
        response = self.client.post(reverse('authentication:login'), {'username': 'pavankumar', 'password': '143Pavan..'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/invalidlogin.html')

    def test_to_activte_user(self):
        """
        Test to get login page.
        """
        response = self.client.post(reverse('authentication:signup'), self.user)
        self.assertEqual(response.status_code, 200)
        user = MyUser.objects.get(pk=response.context['user'].pk)
        self.assertEqual(user.is_active, False)
        activate = self.client.get(reverse('authentication:activate',
                                           kwargs={'uidb64': response.context['uid'], 'token': response.context['token']}))
        self.assertEqual(activate.status_code, 200)
        user = MyUser.objects.get(pk=response.context['user'].pk)
        self.assertEqual(user.is_active, True)
