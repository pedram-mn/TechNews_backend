from django.contrib import admin

from .models import News, Reference, Tag


# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'content',
        'tags',
        'references'
    ]

    list_filter = ['tags']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = [
        'name'
    ]


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    fields = [
        'link',
        'author',
        'date'
    ]
