from django.contrib import admin

from .models import Bookmarks, Folders

# Register your models here.

admin.site.register(Bookmarks)
admin.site.register(Folders)
