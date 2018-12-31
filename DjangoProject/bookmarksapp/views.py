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

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)

    def get_ordering(self):
        if 'sort' in self.request.GET:
            return self.request.GET['sort']
        else:
            return None
