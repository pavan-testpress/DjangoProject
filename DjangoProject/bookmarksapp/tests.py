from django.test import TestCase
from django.shortcuts import reverse

from authenticationapp.models import MyUser
from .models import Folders, Bookmarks


class BookmarksAppTestCase(TestCase):
    user = None

    def setUp(self):
        """
        This function will execute before for each testcase.
        User creation and login will happen.
        Some sample bookmarks and folders will be save in database.
        """
        self.credentials = {
            'username': 'pavan@gmail.com',
            'password': 'pavankumar'
        }
        MyUser.objects.create_user(**self.credentials)
        self.user = self.client.post(reverse('authenticationapp:login'), self.credentials, follow=True).context['user']
        f = Folders.objects.create(
            name="Google",
            created_by=self.user
        )
        y = Folders.objects.create(
            name="Yahoo",
            created_by=self.user
        )

        Bookmarks.objects.create(
            folder=f,
            url="https://www.google.com",
            name='Google Website',
            created_by=self.user
        )

        Bookmarks.objects.create(
            folder=y,
            url="https://www.yahoo.com",
            name='Yahoo Website',
            created_by=self.user
        )

    def tearDown(self):
        """
        Logout the user after finishing every testcase.
        """
        self.client.get(reverse('authenticationapp:logout'))

    def test_folder_list_without_login(self):
        """
        Test folderlist page without logged in the user.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get(reverse('bookmarksapp:index'))
        self.assertRedirects(response, reverse('authenticationapp:login'))

    def test_post_login_page(self):
        """
        Test to Login Page by posting credentials.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.post(reverse('authenticationapp:login'), self.credentials)
        self.assertRedirects(response, reverse('authenticationapp:index'))

    def test_get_folder_list_view(self):
        """
        Test to get folder list page.
        """
        response = self.client.get(reverse('bookmarksapp:folders'))
        folders = Folders.objects.filter(created_by=self.user)
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x, ordered=False)

    def test_get_folder_list_view_by_name(self):
        """
        Test Sorting feature by name in folderlistpage.
        """
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=name")
        folders = Folders.objects.filter(created_by=self.user).order_by('name')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_created_date(self):
        """
        Test sort by created date in folderlist page.
        """
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=-created")
        folders = Folders.objects.filter(created_by=self.user).order_by('-created')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_modified_date(self):
        """
        Test sort by modified date in folderlist page.
        """
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=-modified")
        folders = Folders.objects.filter(created_by=self.user).order_by('-modified')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_unknown_sorting_order(self):
        """
        Testing folderlist page if it is going to default sort by name
        if invalid sorting given to the page.
        """
        response = self.client.get(reverse('bookmarksapp:folders') + "?sort=-modisadasd")
        folders = Folders.objects.filter(created_by=self.user).order_by('name')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def testBookmarksListWithoutLogin(self):
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get(reverse('bookmarksapp:bookmarks', kwargs={'slug': 'google'}))
        self.assertRedirects(response, reverse('authenticationapp:login'))

    def testGetBookmarksListView(self):
        response = self.client.get(reverse('bookmarksapp:bookmarks', kwargs={'slug': 'google'}))
        tempuser = response.context['user']
        bookmarks = Folders.objects.get(slug='google', created_by=tempuser).folder.all()
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x, ordered=False)
