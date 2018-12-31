from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from authenticationapp.models import MyUser


class Folder(TimeStampedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Folder, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Bookmark(TimeStampedModel):
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, related_name='folder', null=True)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bookmark, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
