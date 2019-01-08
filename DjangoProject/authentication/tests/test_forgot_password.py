from django.test import TestCase
from authentication.models import MyUser
from django.shortcuts import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class ForgotPasswordTestCases(TestCase):
    def setUp(self):
        user = {
            'first_name': 'Pavan Kumar',
            'last_name': 'Kuppala',
            'username': 'pavankumar',
            'email': 'pavancse17@gmail.com',
        }
        user = MyUser.objects.create(first_name=user['first_name'], last_name=user['last_name'], username=user['last_name'], email=user['email'], password="'143Pavan..'", is_active=True)

    def test_to_get_forgot_password(self):
        response = self.client.get(reverse("authentication:forgot_password"))
        self.assertTemplateUsed(response, 'authentication/forgot_password.html')

    def test_post_email_forgot_password(self):
        response = self.client.post(reverse("authentication:forgot_password"), {'email': 'pavancse17@gmail.com'})
        self.assertEqual(response.context['domain'], 'testserver')
        self.assertEqual(response.context['uid'],
                         urlsafe_base64_encode(force_bytes(response.context['user'].pk)).decode())

    def test_reseting_password(self):
        response = self.client.post(reverse("authentication:forgot_password"), {'email': 'pavancse17@gmail.com'})
        forgot_page = self.client.get(reverse('authentication:password_reset', kwargs={'uidb64': response.context['uid'], 'token': response.context['token']}))
        self.assertTemplateUsed(forgot_page, 'authentication/forgot_password_form.html')
        forgot = self.client.post(reverse('authentication:password_reset', kwargs={'uidb64': response.context['uid'], 'token': response.context['token']}), {'password1': '143Pavan..', 'password2': '143Pavan..'})
        self.assertRedirects(forgot, reverse('authentication:index'))
