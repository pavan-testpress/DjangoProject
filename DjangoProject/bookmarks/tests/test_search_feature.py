from django.test import TestCase
from django.shortcuts import reverse

from exam import Exam
from exam import fixture, before

from authenticationapp.models import MyUser
from bookmarks.models import Folder, Bookmark


class FolderListTestCase(Exam, TestCase):
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
                name='foldertest' + str(i),
                created_by=self.user
            )
            Bookmark.objects.create(
                folder=folder,
                url='https://www.google.com',
                name='bookmarktest' + str(i),
                created_by=self.user
            )
            folder = Folder.objects.create(
                name='googletest' + str(i),
                created_by=self.user
            )
            Bookmark.objects.create(
                folder=folder,
                url='https://www.google.com',
                name='bgoogletest' + str(i),
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

    def test_get_folder_list_for_searched_folder(self):
        """
        Test searching feature by name in folderlistpage.
        """
        response = self.client.get(reverse('bookmarks:folders') + "?sort=name&name=test")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='test').order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 10)

        response = self.client.get(reverse('bookmarks:folders') + "?sort=-modified&name=test")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='test').order_by('-modified')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 10)

        response = self.client.get(reverse('bookmarks:folders') + "?sort=-created&name=test")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='test').order_by('-created')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 10)

        response = self.client.get(reverse('bookmarks:folders') + "?sort=name&name=yahoo")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='yahoo').order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 1)

        response = self.client.get(reverse('bookmarks:folders') + "?sort=name&name=asdad")
        folders = Folder.objects.filter(created_by=self.user, name__icontains='asdad').order_by('name')[:10]
        self.assertQuerysetEqual(response.context['folders'], folders, transform=lambda x: x)
        self.assertEqual(response.context['folders'].count(), 0)

    def test_get_bookmark_list_for_searched_bookmark(self):
        """
        Test searching feature by name in bookmarks list page.
        """
        response = self.client.get(reverse('bookmarks:folder-bookmarks',
                                           kwargs={'slug': 'foldertest1'}) + "?sort=name&name=test")
        folder = Folder.objects.get(created_by=self.user, name='foldertest1')
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=folder, name__icontains='test')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 1)

        response = self.client.get(reverse('bookmarks:folder-bookmarks',
                                           kwargs={'slug': 'yahoo'}) + "?sort=-created&name=oo")
        folder = Folder.objects.get(created_by=self.user, name='Yahoo')
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=folder,
                                            name__icontains='oo').order_by('-created')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 2)

        response = self.client.get(reverse('bookmarks:folder-bookmarks',
                                           kwargs={'slug': 'yahoo'}) + "?sort=-modified&name=oo")
        folder = Folder.objects.get(created_by=self.user, name='Yahoo')
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=folder, name__icontains='oo').order_by(
            '-modified')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 2)

        response = self.client.get(reverse('bookmarks:folder-bookmarks',
                                           kwargs={'slug': 'foldertest1'}) + "?sort=name&name=test")
        folder = Folder.objects.get(created_by=self.user, name='foldertest1')
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=folder, name__icontains='test')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 1)

        response = self.client.get(reverse('bookmarks:folder-bookmarks',
                                           kwargs={'slug': 'foldertest1'}) + "?sort=name&name=test")
        folder = Folder.objects.get(created_by=self.user, name='foldertest1')
        bookmarks = Bookmark.objects.filter(created_by=self.user, folder=folder, name__icontains='test')[:10]
        self.assertQuerysetEqual(response.context['bookmarks'], bookmarks, transform=lambda x: x)
        self.assertEqual(response.context['bookmarks'].count(), 1)
