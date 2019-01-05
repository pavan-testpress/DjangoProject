import django_filters

from .models import Folder, Bookmark


class FolderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Folder
        fields = ['name']


class BookmarkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Bookmark
        fields = ['name']
