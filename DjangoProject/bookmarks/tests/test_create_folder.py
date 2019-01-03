from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder


class CreateFolderTestCase(Exam, TestCase):

    @fixture
    def user(self):
        return MyUser.objects.create_user(username="pavan@gmail.com", password="pavankumar")

    @before
    def inserting_sample_data(self):
        """
        This function will execute before for each testcase.
        Some sample bookmarks and folders will be saved in database.
        """
        Folder.objects.create(
            name='Google',
            created_by=self.user
        )

    @before
    def login(self):
        self.client.post('/login/?next=/bookmarks/folders/create', {'username': 'pavan@gmail.com', 'password': 'pavankumar'})

    def test_redirect_if_not_logged_in(self):
        """
        Test if folder create page without logged in the user
        redirects to login or not.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get('/bookmarks/folders/create/')
        self.assertRedirects(response, '/login/?next=/bookmarks/folders/create/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmarks/folders/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:create-folder'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:create-folder'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/folder_form.html')

    def test_creating_existing_folder(self):
        response = self.client.post(reverse('bookmarks:create-folder'), {'name': 'Google'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/invalid_folder_form.html')
        self.assertEqual(response.context['error'], 'Google already exists..')

    def test_creating_new_folder(self):
        response = self.client.post(reverse('bookmarks:create-folder'), {'name': 'Yoogle'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bookmarks/folders/')
        assert Folder.objects.filter(name='Yoogle', created_by=self.user).exists()
