from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder, Bookmark


class UpdateFolderTestCase(Exam, TestCase):

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
        Folder.objects.create(
            name='Yahoo',
            created_by=self.user
        )

    @before
    def login(self):
        self.client.post('/login/?next=/bookmarks/folders/google/edit/', {'username': 'pavan@gmail.com', 'password': 'pavankumar'})

    def test_redirect_if_not_logged_in(self):
        """
        Test if folder edit page without logged in the user
        redirects to login or not.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get('/bookmarks/folders/google/edit/')
        self.assertRedirects(response, '/login/?next=/bookmarks/folders/google/edit/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmarks/folders/google/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:folder-edit', kwargs={'slug': 'google'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:folder-edit', kwargs={'slug': 'google'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_update_form.html')

    def test_editing_with_existing_folder(self):
        response = self.client.post(reverse('bookmarks:folder-edit', kwargs={'slug': 'google'}), {'name': 'Yahoo'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/invalid_folder_form.html')
        self.assertEqual(response.context['error'], 'Yahoo already exists..')

    def test_edit_folder(self):
        response = self.client.post(reverse('bookmarks:folder-edit', kwargs={'slug': 'google'}), {'name': 'hoogle'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bookmarks/folders/hoogle/')
        assert Folder.objects.filter(name='hoogle', created_by=self.user).exists()
        self.assertEqual(Folder.objects.get(name='hoogle', created_by=self.user).folder.count(), 1)
