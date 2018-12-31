from django.test import TestCase
from django.shortcuts import reverse

from authenticationapp.models import MyUser
from .models import Folders, Bookmarks


class BookmarksAppTestCase(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'pavan@gmail.com',
            'password': 'pavankumar'
        }
        MyUser.objects.create_user(**self.credentials)
        user = self.client.post(reverse('authenticationapp:login'), self.credentials, follow=True).context['user']
        f = Folders.objects.create(
            name="Google",
            created_by=user
        )
        y = Folders.objects.create(
            name="Yahoo",
            created_by=user
        )

        Bookmarks.objects.create(
            folder=f,
            url="https://www.google.com",
            name='Google Website',
            created_by=user
        )

        Bookmarks.objects.create(
            folder=y,
            url="https://www.yahoo.com",
            name='Yahoo Website',
            created_by=user
        )

    def test_folder_list_without_login(self):
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get(reverse('bookmarksapp:index'))
        self.assertRedirects(response, reverse('authenticationapp:login'))

    def test_post_login_page(self):
        response = self.client.post(reverse('authenticationapp:login'), self.credentials)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def test_get_folder_list_view(self):
        response = self.client.get(reverse('bookmarksapp:folders'))
        user = response.context['user']
        folders = Folders.objects.filter(created_by=user)
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x, ordered=False)

    def test_get_folder_list_view_by_name(self):
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=name")
        user = response.context['user']
        folders = Folders.objects.filter(created_by=user)
        folders = folders.order_by('name')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_created_date(self):
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=-created")
        user = response.context['user']
        folders = Folders.objects.filter(created_by=user)
        folders = folders.order_by('-created')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_modified_date(self):
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=-modified")
        user = response.context['user']
        folders = Folders.objects.filter(created_by=user)
        folders = folders.order_by('-modified')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
