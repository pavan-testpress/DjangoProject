from django.shortcuts import reverse, render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                sort = 'name'
                return sort
            return sort
        else:
            return None


@method_decorator(login_required, name="dispatch")
class FolderCreateView(CreateView, FolderListView):
    model = Folders
    fields = ['name', ]
    template_name = 'bookmarksapp/folderlist.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.created_by = self.request.user
        if Folders.objects.filter(name__iexact=form.name, created_by=form.created_by).exists():
            error_message = 'Folder with name ' + str(form.name).capitalize() + ' already exists'
            folders = Folders.objects.filter(created_by=self.request.user)
            return render(self.request, 'bookmarksapp/folderexists.html',
                          {'error_message': error_message, 'folders': folders})
        # try:
        #     from.created_by = self.request.user
        #     form.save()
        # except ValidationError as e:
        #     folders = Folders.objects.filter(created_by=self.request.user)
        #     return render(self.request, 'bookmarksapp/folderexists.html',
        #                   {'error_message': e, 'folders': folders})

        else:
            form.save()
            return HttpResponseRedirect(reverse('bookmarksapp:folders'))
