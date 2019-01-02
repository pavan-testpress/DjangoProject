from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Folders


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bookmarksapp:folders'))
    else:
        return HttpResponseRedirect(reverse('authenticationapp:login'))


@method_decorator(login_required, name="dispatch")
class FolderListView(ListView):
    model = Folders
    context_object_name = 'folders'
    template_name = 'bookmarksapp/folderlist.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)

    def get_ordering(self):
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                return 'name'
            return sort
        return None


@method_decorator(login_required, name="dispatch")
class BookmarksListView(ListView):
    model = Folders
    context_object_name = 'bookmarks'
    template_name = 'bookmarksapp/bookmarks-list.html'

    def get_queryset(self):
        if 'sort' in self.request.GET:
            self.queryset = Folders.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder
            qs = super(BookmarksListView, self).get_queryset()
        else:
            qs = Folders.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder.all()
        return qs

    def get_ordering(self):
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                return 'name'
            return sort
        return None
