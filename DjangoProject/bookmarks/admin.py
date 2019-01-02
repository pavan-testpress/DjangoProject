from django.contrib import admin

from .models import Bookmark, Folder

admin.site.register(Bookmark)
admin.site.register(Folder)
