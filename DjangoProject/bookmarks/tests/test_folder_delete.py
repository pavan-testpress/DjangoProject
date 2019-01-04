from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder, Bookmark


class DeleteFolderTestCase(Exam, TestCase):

    @fixture
    def user(self):
        return MyUser.objects.create_user(username="pavan@gmail.com", password="pavankumar")

    @before
    def inserting_sample_data(self):
        """
        This function will execute before for each testcase.
        Some sample bookmarks and folders will be saved in database.
        """
        f = Folder.objects.create(
            name='Google',
            created_by=self.user
        )
        Bookmark.objects.create(
            folder=f,
            url='https://www.google.com',
            name='google',
            created_by=self.user
        )
        y = Folder.objects.create(
            name='Yahoo',
            created_by=self.user
        )
        Bookmark.objects.create(
            folder=y,
            url='https://www.yoogle.com',
            name='yoogle',
            created_by=self.user
        )
        Bookmark.objects.create(
            folder=y,
            url='https://www.google.com',
            name='yoogle',
            created_by=self.user
        )

    @before
    def login(self):
        self.client.post('/login/?next=/bookmarks/folders/1/delete/', {'username': 'pavan@gmail.com', 'password': 'pavankumar'})

    def test_redirect_if_not_logged_in(self):
        """
        Test if folder delete page without logged in the user
        redirects to login or not.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get('/bookmarks/folders/1/delete/')
        self.assertRedirects(response, '/login/?next=/bookmarks/folders/1/delete/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmarks/folders/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folder-delete', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folder-delete', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_delete_confirm.html')

    def test_first_delete_folder(self):
        """
        Checking behaviour of first folder.
            - It should create a new Uncategorised folder.
            - It should move all bookmarks present inside that folder to Uncategorised.
        """
        self.assertEqual(Folder.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(pk=1).folder.name, 'Google')
        response = self.client.post(reverse('bookmarks:folder-delete', kwargs={'pk': '1'}))
        assert Folder.objects.filter(name='UnCategorised', created_by=self.user).exists()
        self.assertEqual(Bookmark.objects.get(pk=1).folder.name, 'UnCategorised')
        self.assertRedirects(response, '/bookmarks/folders/')
        self.assertEqual(Folder.objects.count(), 2)
        self.client.post(reverse('bookmarks:folder-delete', kwargs={'pk': '2'}))
        self.assertEqual(Folder.objects.count(), 1)

    def test_delete_when_UnCategorised_folder_exists(self):
        """
        Checking behaviour of when UnCategorised folder exists.
            - It should move bookmarks to UnCategorised folder
                such that no duplicate data is being inserted for logged in User.
            - Checking Count of Uncategorised folder when folder having duplicates is deleted.
            - Checking Count of Uncategorised folder when folder with no duplicate is deleted.
        """
        f = Folder.objects.create(name="UnCategorised", slug="uncategorised", created_by=self.user)
        response = self.client.post(reverse('bookmarks:folder-delete', kwargs={'pk': '1'}))
        self.assertRedirects(response, '/bookmarks/folders/')
        self.assertEqual(f.folder.count(), 1)
        self.client.post(reverse('bookmarks:folder-delete', kwargs={'pk': '2'}))
        self.assertEqual(f.folder.count(), 2)
