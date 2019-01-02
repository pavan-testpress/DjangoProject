from django.test import TestCase
from django.shortcuts import reverse

from faker import Faker

from authenticationapp.models import MyUser
from .models import Folder, Bookmark


class BookmarksTestCase(TestCase):
    user = None
    fake = Faker()

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

        for i in range(20):
            f = Folder.objects.create(
                name=self.fake.name(),
                created_by=self.user
            )
            Bookmark.objects.create(
                folder=f,
                url=self.fake.name(),
                name=self.fake.name(),
                created_by=self.user
            )
        f = Folder.objects.create(
            name="Google",
            created_by=self.user
        )

        y = Folder.objects.create(
            name="Yahoo",
            created_by=self.user
        )

        Bookmark.objects.create(
            folder=f,
            url="https://www.google.com",
            name='Google Website',
            created_by=self.user
        )

        Bookmark.objects.create(
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
        response = self.client.get(reverse('bookmarks:index'))
        self.assertRedirects(response, reverse('authenticationapp:login'))

    def test_get_folder_list_view(self):
        """
        Test to get folder list page.
        """
        response = self.client.get(reverse('bookmarks:folders'))
        folders = Folder.objects.filter(created_by=self.user)
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x, ordered=False)

    def test_get_folder_list_view_by_name(self):
        """
        Test Sorting feature by name in folderlistpage.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=name")
        folders = Folder.objects.filter(created_by=self.user).order_by('name')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_created_date(self):
        """
        Test sort by created date in folderlist page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-created")
        folders = Folder.objects.filter(created_by=self.user).order_by('-created')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_modified_date(self):
        """
        Test sort by modified date in folderlist page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modified")
        folders = Folder.objects.filter(created_by=self.user).order_by('-modified')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_unknown_sorting_order(self):
        """
        Testing folderlist page if it is going to default sort by name
        if invalid sorting given to the page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modisadasd")
        folders = Folder.objects.filter(created_by=self.user).order_by('name')
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
