from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from authenticationapp.models import MyUser


class Folders(TimeStampedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Folders, self).save(*args, **kwargs)

    # def clean(self):
    #     super(Folders, self).clean()
    #     if Folders.objects.filter(name__iexact=self.name, created_by=self.created_by).exists():
    #         raise ValidationError('Folder exists')

    def __str__(self):
        return self.name


class Bookmarks(TimeStampedModel):
    folder = models.ForeignKey(Folders, on_delete=models.SET_NULL, related_name='folder', null=True)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Bookmarks, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
