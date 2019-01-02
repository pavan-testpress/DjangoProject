from django.urls import path

from . import views

app_name = "bookmarks"

urlpatterns = [
    path('', views.index, name="index"),
    path('folders/', views.FolderListView.as_view(), name="folders"),
<<<<<<< HEAD:DjangoProject/bookmarks/urls.py
    path('folders/<slug>/', views.BookmarksListView.as_view(), name="folder-bookmarks")
=======
    path('folders/create/', views.FolderCreateView.as_view(), name="create_folder"),
    path('folders/<slug>/', views.BookmarksListView.as_view(), name="bookmarks"),
>>>>>>> edca14b... Add Login decorator:DjangoProject/bookmarksapp/urls.py
]
