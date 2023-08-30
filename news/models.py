from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Reference(models.Model):
    link = models.CharField(max_length=1000, unique=True, default=None)
    author = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return self.link


class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    references = models.ManyToManyField(Reference)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'
