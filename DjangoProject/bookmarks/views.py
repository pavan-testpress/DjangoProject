from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.core.paginator import Paginator

from .models import Folder


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bookmarks:folders'))
    else:
        return HttpResponseRedirect(reverse('authenticationapp:login'))


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