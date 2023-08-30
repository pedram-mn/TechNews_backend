import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import News, Reference, Tag


class NewsViewTestCase(TestCase):
    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Create test data
        self.tag1 = Tag.objects.create(name='Tag 1')
        self.tag2 = Tag.objects.create(name='Tag 2')

        self.reference1 = Reference.objects.create(link='Reference 1',
                                                   author='test name one',
                                                   date=datetime.datetime.now())
        self.reference2 = Reference.objects.create(link='Reference 2',
                                                   author='test name two',
                                                   date=datetime.datetime(2021, 1, 1))

        self.news1 = News.objects.create(title='News 1', content='Content 1')
        self.news1.tags.add(self.tag1, self.tag2)
        self.news1.references.add(self.reference1, self.reference2)

        self.news2 = News.objects.create(title='News 2', content='Content 2')
        self.news2.tags.add(self.tag1)
        self.news2.references.add(self.reference1)

    def test_get_news(self):
        response = self.client.get('/api/news/get/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_tags(self):
        # Test filtering news by tags using URL parameters
        response = self.client.get('/api/news/get/', {'tags': f"{self.tag2.name}"})  # tag2 only exist in news1

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the correct number of news items
        self.assertEqual(len(response.data), 1)

        # Check if the returned news item has the correct tags
        self.assertEqual(len(response.data[0]['tags']), 2)
        self.assertIn(self.tag1.name, response.data[0]['tags'])
        self.assertIn(self.tag2.name, response.data[0]['tags'])

    def test_filter_by_tags_no_results(self):
        # Test filtering news by tags that have no matches
        response = self.client.get('/api/news/get/', {'tags': f"{self.tag1.name + 'asd'}"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response is empty since there should be no matches
        self.assertEqual(len(response.data), 0)
