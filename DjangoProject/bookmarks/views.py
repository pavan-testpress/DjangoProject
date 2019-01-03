from django.shortcuts import reverse, render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Folder


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bookmarks:folders'))
    else:
        return HttpResponseRedirect(reverse('authenticationapp:login'))


@method_decorator(login_required, name='dispatch')
class FolderListView(ListView):
    model = Folder
    context_object_name = 'folders'
    template_name = 'bookmarks/folderlist.html'
    paginate_by = 10

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

    def get_context_data(self):
        data = super(FolderListView, self).get_context_data()
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                data['sort'] = 'name'
            data['sort'] = sort
        return data


@method_decorator(login_required, name="dispatch")
class BookmarksListView(ListView):
    model = Folder
    context_object_name = 'bookmarks'
    template_name = 'bookmarks/bookmarks-list.html'
    paginate_by = 10

    def get_queryset(self):
        if 'sort' in self.request.GET:
            self.queryset = Folder.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder
            qs = super(BookmarksListView, self).get_queryset()
        else:
            qs = Folder.objects.get(created_by=self.request.user, slug=self.kwargs['slug']).folder.all()
        return qs

    def get_ordering(self):
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                return 'name'
            return sort
        return 'None'

    def get_context_data(self):
        data = super(BookmarksListView, self).get_context_data()
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort not in ['-modified', '-created', 'name']:
                data['sort'] = 'name'
            data['sort'] = sort
        return data


@method_decorator(login_required, name="dispatch")
class FolderCreateView(CreateView):
    model = Folder
    fields = ['name', ]

    def form_valid(self, form):
        if Folder.objects.filter(name__iexact=form.cleaned_data['name'], created_by=self.request.user).exists():
            error = form.cleaned_data['name'] + " already exists.."
            return render(self.request, 'bookmarks/invalid_folder_form.html', {'error': error})
        else:
            form = form.save(commit=False)
            form.created_by = self.request.user
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:folders'))
