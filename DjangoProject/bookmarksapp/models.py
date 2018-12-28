from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from authenticationapp.models import MyUser

# Create your models here.


class Folders(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Folders, self).save(*args, **kwargs)


class Bookmarks(TimeStampedModel):
    folder = models.ForeignKey(Folders, on_delete=models.SET_NULL, related_name='folder', null=True)
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField(max_length=200, unique=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bookmarks, self).save(*args, **kwargs)
