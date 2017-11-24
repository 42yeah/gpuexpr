from django.db import models
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Passage(models.Model):
    title = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024)
    body = RichTextUploadingField()
    tags = models.CharField(max_length=1024)

    def __str__(self):
        return self.author + ': ' + self.title

class Pic(models.Model):
    name = models.CharField(max_length=1024)
    f = models.FileField()

    def __str__(self):
        return self.name
