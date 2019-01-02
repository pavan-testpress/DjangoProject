from django.urls import path

from . import views

app_name = "bookmarksapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('folders/', views.FolderListView.as_view(), name="folders"),
    path('folders/create/', views.FolderCreateView.as_view(), name="create_folder"),
    path('folders/<slug>/', views.BookmarksListView.as_view(), name="bookmarks"),
]
