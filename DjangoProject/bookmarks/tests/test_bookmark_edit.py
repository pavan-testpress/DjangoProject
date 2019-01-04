from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder, Bookmark


class UpdateBookmarkTestCase(Exam, TestCase):

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
        Bookmark.objects.create(
            folder=f,
            url='https://www.yoogle.com',
            name='yoogle',
            created_by=self.user
        )
        Folder.objects.create(
            name='Yahoo',
            created_by=self.user
        )

    @before
    def login(self):
        self.client.post('/login/?next=/bookmarks/folders/google/1/edit/', {'username': 'pavan@gmail.com', 'password': 'pavankumar'})

    def test_redirect_if_not_logged_in(self):
        """
        Test if bookmark edit page without logged in the user
        redirects to login or not.
        """
        self.client.get(reverse('authenticationapp:logout'))
        response = self.client.get('/bookmarks/folders/google/1/edit/')
        self.assertRedirects(response, '/login/?next=/bookmarks/folders/google/1/edit/')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmarks/folders/google/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmarks:bookmark-edit', kwargs={'slug': 'google', 'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmarks:bookmark-edit', kwargs={'slug': 'google', 'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/bookmark_update_form.html')

    def test_editing_with_existing_bookmark(self):
        response = self.client.post(reverse('bookmarks:bookmark-edit', kwargs={'slug': 'google', 'pk': 1}),
                                    {'name': 'Yoogle', 'url': 'https://www.yoogle.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmarks/invalid_update_bookmark.html')
        self.assertEqual(response.context['error'], 'Yoogle with https://www.yoogle.com already exists..')

    def test_edit_bookmark(self):
        response = self.client.post(reverse('bookmarks:bookmark-edit', kwargs={'slug': 'google', 'pk': 1}),
                                    {'name': 'Toogle', 'url': 'https://www.toogle.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bookmarks/folders/google/')
        assert Bookmark.objects.filter(name='Toogle',
                                       url="https://www.toogle.com",
                                       created_by=self.user).exists()
