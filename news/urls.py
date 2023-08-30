from django.urls import path

from .views import NewsList

urlpatterns = [
    path('get/', NewsList.as_view(), name="get_news"),
]
