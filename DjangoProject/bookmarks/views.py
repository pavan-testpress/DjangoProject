from django.shortcuts import reverse, render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Folder, Bookmark


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


@method_decorator(login_required, name="dispatch")
class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['name', 'url']
    template_name = 'bookmarks/bookmark_form.html'

    def form_valid(self, form):
        folder = Folder.objects.get(slug=self.kwargs['slug'], created_by=self.request.user)
        if Bookmark.objects.filter(name__iexact=form.cleaned_data['name'],
                                   url__iexact=form.cleaned_data['url'],
                                   created_by=self.request.user,
                                   folder=folder).exists():
            error = form.cleaned_data['name'] + " with " + form.cleaned_data['url'] + " already exists.."
            return render(self.request, 'bookmarks/invalid_bookmark_form.html', {'error': error})
        else:
            form = form.save(commit=False)
            form.created_by = self.request.user
            form.folder = folder
            form.save()
            return HttpResponseRedirect(reverse('bookmarks:folder-bookmarks', kwargs={'slug': folder.slug}))


@method_decorator(login_required, name="dispatch")
class FolderUpdateView(UpdateView):
    model = Folder
    fields = ['name']
    template_name = 'bookmarks/folder_update_form.html'

    def form_valid(self, form):
        if Folder.objects.filter(name__iexact=form.cleaned_data['name'], created_by=self.request.user).exists():
            f = Folder.objects.filter(name__iexact=form.cleaned_data['name'], created_by=self.request.user).first()
            error = form.cleaned_data['name'] + " already exists.."
            return render(self.request, 'bookmarks/invalid_folder_update_form.html',
                          context={'error': error, 'object': f, 'form': form})
        else:
            return super(FolderUpdateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['name', 'url']
    template_name = 'bookmarks/bookmark_update_form.html'

    def form_valid(self, form):
        folder = Folder.objects.get(slug=self.kwargs['slug'], created_by=self.request.user)
        if (Bookmark.objects.filter(url__iexact=form.cleaned_data['url'],
                                    created_by=self.request.user,
                                    folder=folder).exists()) or (Bookmark.objects.filter(
                                                                name__iexact=form.cleaned_data['name'],
                                                                created_by=self.request.user,
                                                                folder=folder).exists()):
            error = form.cleaned_data['name'] + " with " + form.cleaned_data['url'] + " already exists.."
            return render(self.request, 'bookmarks/invalid_update_bookmark.html',
                          {'error': error, 'form': form, 'object': self.object})
        else:
            return super(BookmarkUpdateView, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class FolderDeleteView(DeleteView):
    model = Folder
    template_name = 'bookmarks/folder_delete_confirm.html'

    def delete(self, request, *args, **kwargs):
        delete_folder = self.get_object()
        if Folder.objects.filter(name='UnCategorised', created_by=self.request.user).exists():
            f = Folder.objects.get(name="UnCategorised", created_by=self.request.user)
            for bookmark in delete_folder.folder.all():
                if (f.folder.filter(url__iexact=bookmark.url, created_by=self.request.user).exists())or\
                        (f.folder.filter(name__iexact=bookmark.name, created_by=self.request.user).exists()):
                    bookmark.delete()
                else:
                    bookmark.folder = f
                    bookmark.save()
        else:
            f = Folder.objects.create(name='UnCategorised', created_by=self.request.user)
            for bookmark in delete_folder.folder.all():
                bookmark.folder = f
                bookmark.save()
        delete_folder.delete()
        return HttpResponseRedirect(reverse('bookmarks:folders'))


@method_decorator(login_required, name="dispatch")
class BookmarkDeleteView(DeleteView):
    model = Bookmark
    template_name = 'bookmarks/bookmark_delete_confirm.html'

    def get_success_url(self):
        return reverse('bookmarks:folder-bookmarks', kwargs={'slug': self.object.folder.slug})
