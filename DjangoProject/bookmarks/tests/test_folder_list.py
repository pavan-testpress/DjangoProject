from django.test import TestCase
from django.shortcuts import reverse

from faker import Faker
from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder, Bookmark


class FolderListTestCase(Exam, TestCase):
    fake = Faker()
    user = None

    @fixture
    def user(self):
        return MyUser.objects.create_user(username="pavan@gmail.com", password="pavankumar")

    @before
    def inserting_sample_data_and_login_user(self):
        """
        This function will execute before for each testcase.
        Some sample bookmarks and folders will be saved in database.
        """
        for i in range(20):
            folder = Folder.objects.create(
                name=self.fake.name(),
                created_by=self.user
            )
            Bookmark.objects.create(
                folder=folder,
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

    @before
    def login(self):
        self.client.post('/login/?next=/bookmarks/folders/', {'username': 'pavan@gmail.com', 'password': 'pavankumar'})

    def test_redirect_if_not_logged_in(self):
        """
        Test folderlist page without logged in the user.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertRedirects(response, '/login/?next=/bookmarks/folders/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmarks/folders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folderlist.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('bookmarks:folders'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['folders']) == 10)

    def test_lists_all_folders(self):
        """
            Test Sorting feature by name in bookmark list page.
        """
        response = self.client.get(reverse('bookmarks:folders') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['folders']) == 2)

    def test_get_folder_list_view_by_name(self):
        """
        Test Sorting feature by name in folderlistpage.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=name")
        folders = Folder.objects.filter(created_by=self.user).order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_created_date(self):
        """
        Test sort by created date in folderlist page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-created")
        folders = Folder.objects.filter(created_by=self.user).order_by('-created')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_view_by_modified_date(self):
        """
        Test sort by modified date in folderlist page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modified")
        folders = Folder.objects.filter(created_by=self.user).order_by('-modified')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)

    def test_get_folder_list_unknown_sorting_order(self):
        """
        Testing folderlist page if it is going to default sort by name
        if invalid sorting given to the page.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modisadasd")
        folders = Folder.objects.filter(created_by=self.user).order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
