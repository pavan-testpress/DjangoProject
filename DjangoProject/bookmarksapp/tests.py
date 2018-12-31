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
        tempuser = self.client.post(reverse('authenticationapp:login'), self.credentials, follow=True).context['user']
        f = Folders.objects.create(
            name="Google",
            created_by=tempuser
        )
        y = Folders.objects.create(
            name="Yahoo",
            created_by=tempuser
        )

        Bookmarks.objects.create(
            folder=f,
            url="https://www.google.com",
            name='Google Website',
            created_by=tempuser
        )

        Bookmarks.objects.create(
            folder=y,
            url="https://www.yahoo.com",
            name='Yahoo Website',
            created_by=tempuser
        )

    def testFolderListWithoutLogin(self):
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get(reverse('bookmarksapp:index'))
        self.assertRedirects(response, reverse('authenticationapp:login'))

    def testPostLoginPage(self):
        response = self.client.post(reverse('authenticationapp:login'), self.credentials)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def testGetFolderListView(self):
        response = self.client.get(reverse('bookmarksapp:folders'))
        tempuser = response.context['user']
        folders = Folders.objects.filter(created_by=tempuser)
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x, ordered=False)

    def testGetFolderListViewByName(self):
        response = self.client.get(reverse('bookmarksapp:folders')+"?sort=name")
        tempuser = response.context['user']
        folders = Folders.objects.filter(created_by=tempuser)
        folders = folders.order_by('name')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def testGetFolderListViewByCreatedDate(self):
        response = self.client.get(reverse('bookmarksapp:folders')+"?sort=-created")
        tempuser = response.context['user']
        folders = Folders.objects.filter(created_by=tempuser)
        folders = folders.order_by('-created')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def testGetFolderListViewByModifiedDate(self):
        response = self.client.get(reverse('bookmarksapp:folders')+"?sort=-modified")
        tempuser = response.context['user']
        folders = Folders.objects.filter(created_by=tempuser)
        folders = folders.order_by('-modified')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
