# books/tests.py
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author, Language

class BookAPITests(APITestCase):
    def setUp(self):
        # Create test data
        self.author = Author.objects.create(name="Test Author")
        self.language = Language.objects.create(name="en")
        self.book = Book.objects.create(
            title="Test Book",
            downloads=100
        )
        self.book.authors.add(self.author)
        self.book.languages.add(self.language)

    def test_book_list(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_book_filter_language(self):
        response = self.client.get('/api/books/?language=en')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_book_filter_topic(self):
        response = self.client.get('/api/books/?topic=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
