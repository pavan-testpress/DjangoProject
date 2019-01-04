from django.test import TestCase
from django.shortcuts import reverse

from faker import Faker
from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder, Bookmark


class BookmarksTestCase(Exam, TestCase):
    fake = Faker()
    user = None

    @fixture
    def user(self):
        return MyUser.objects.create_user(username="pavan@gmail.com", password="pavankumar")

    @before
    def inserting_sample_data(self):
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
        for i in range(20):
            Bookmark.objects.create(
                folder=f,
                url="https://www.google.com" + str(i),
                name='Google Website' + str(i),
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
        Test Bookmark list page without logged in the user.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get('/bookmarks/folders/google/')
        self.assertRedirects(response, '/login/?next=/bookmarks/folders/google/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmarks/folders/google/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmarks-list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['bookmarks']) == 10)

    def test_lists_all_folders(self):
        """
        Get third page and confirm it has (exactly) remaining 3 items
        """
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}) + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['bookmarks']) == 1)

    def test_get_bookmark_list_view_by_name(self):
        """
        Test Sorting feature by name in bookmark list page.
        """
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}) + "?sort=name")
        bookmarks = Folder.objects.get(slug='google', created_by=self.user).folder.all().order_by('name')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmark_list_view_by_created_date(self):
        """
        Test sort by created date in bookmark list page.
        """
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}) + "?sort=-created")
        bookmarks = Folder.objects.get(slug='google', created_by=self.user).folder.all().order_by('-created')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmark_list_view_by_modified_date(self):
        """
        Test sort by modified date in bookmark list page.
        """
        response = self.client.get(reverse('bookmarks:folder-bookmarks', kwargs={'slug': 'google'}) + "?sort=-modified")
        bookmarks = Folder.objects.get(slug='google', created_by=self.user).folder.all().order_by('-modified')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)

    def test_get_bookmark_list_unknown_sorting_order(self):
        """
        Testing bookmark list page if it is going to default sort by name
        if invalid sorting given to the page.
        """
        response = self.client.get(reverse('bookmarks:folder-bookmarks',
                                           kwargs={'slug': 'google'}) + "?sort=-dsfdfdsfsdf")
        bookmarks = Folder.objects.get(slug='google', created_by=self.user).folder.all().order_by('name')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
