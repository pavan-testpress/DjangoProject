from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
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
    template_name = 'bookmarks/folder_list.html'
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
            return 'name'
