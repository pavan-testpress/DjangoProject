from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from .models import Folders


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bookmarksapp:folders'))
    else:
        return HttpResponseRedirect(reverse('authenticationapp:login'))


class FolderListView(ListView):
    model = Folders
    context_object_name = 'folders'
    template_name = 'bookmarksapp/folderlist.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(FolderListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('authenticationapp:login'))

    def get_queryset(self):
        qs = super().get_queryset()
        print(qs.filter(created_by=self.request.user))
        return qs.filter(created_by=self.request.user)

    def get_ordering(self):
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                sort = 'name'
                return sort
            return sort
        else:
            return None


class BookmarksListView(ListView):
    model = Folders
    context_object_name = 'bookmarks'
    template_name = 'bookmarksapp/bookmarkslist.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(BookmarksListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('authenticationapp:login'))

    def get_queryset(self):
        if 'sort' in self.request.GET:
            self.queryset = Folders.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder
            qs = super(BookmarksListView, self).get_queryset()
        else:
            qs = Folders.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder.all()
        return qs

    def get_ordering(self):
        if 'sort' in self.request.GET:
            return self.request.GET['sort']
        else:
            return None


class BookmarksListView(ListView):
    model = Folders
    context_object_name = 'bookmarks'
    template_name = 'bookmarksapp/bookmarkslist.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(BookmarksListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('authenticationapp:login'))

    def get_queryset(self):
        if 'sort' in self.request.GET:
            self.queryset = Folders.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder
            qs = super(BookmarksListView, self).get_queryset()
        else:
            qs = Folders.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder.all()
        return qs

    def get_ordering(self):
        if 'sort' in self.request.GET:
            return self.request.GET['sort']
        else:
            return None
