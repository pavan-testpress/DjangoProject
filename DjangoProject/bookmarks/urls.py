from django.urls import path

from . import views

app_name = "bookmarks"

urlpatterns = [
    path('', views.index, name="index"),
    path('folders/', views.FolderListView.as_view(), name="folders"),
    path('folders/create/', views.FolderCreateView.as_view(), name="create-folder"),
    path('folders/<slug>/', views.BookmarksListView.as_view(), name="folder-bookmarks"),
    path('folders/<slug>/edit/', views.FolderUpdateView.as_view(), name="folder-edit"),
    path('folders/<pk>/delete/', views.FolderDeleteView.as_view(), name="folder-delete"),
    path('folders/<slug>/create/', views.BookmarkCreateView.as_view(), name="create-bookmark"),
    path('folders/<slug>/<pk>/edit/', views.BookmarkUpdateView.as_view(), name="bookmark-edit"),
    path('folders/<slug>/<pk>/delete/', views.BookmarkDeleteView.as_view(), name="bookmark-delete"),
]
