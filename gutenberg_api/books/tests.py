# books/tests.py
from rest_framework.test import APITestCase
from rest_framework import status

class BookAPITests(APITestCase):
    """Test the books API endpoints"""

    def test_api_endpoint_accessible(self):
        """Test if the API endpoint is accessible"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)

    def test_response_structure(self):
        """Test if API response has the correct structure"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if response.data['results']:
            book = response.data['results'][0]
            # Check required fields exist
            required_fields = [
                'id', 'gutenberg_id', 'title', 'authors', 'languages',
                'subjects', 'bookshelves', 'formats', 'download_count',
                'media_type'
            ]
            for field in required_fields:
                self.assertIn(field, book)

    def test_pagination(self):
        """Test if pagination is working"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 25)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_filter_fields_exist(self):
        """Test if all filter options are available"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test each filter endpoint
        filter_endpoints = [
            '/api/books/?language=en',
            '/api/books/?mime_type=text/plain',
            '/api/books/?topic=fiction',
            '/api/books/?author=twain',
            '/api/books/?title=yankee',
            '/api/books/?book_ids=86'
        ]

        for endpoint in filter_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_multiple_filters(self):
        """Test if multiple filters can be combined"""
        response = self.client.get('/api/books/?language=en&topic=fiction')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download_count_sorting(self):
        """Test if books are sorted by download count"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if len(response.data['results']) > 1:
            first_book = response.data['results'][0]
            second_book = response.data['results'][1]
            self.assertGreaterEqual(
                first_book['download_count'],
                second_book['download_count']
            )

    def test_author_structure(self):
        """Test author information structure"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if response.data['results']:
            book = response.data['results'][0]
            if book['authors']:
                author = book['authors'][0]
                self.assertIn('name', author)
                if 'birth_year' in author:
                    self.assertIsInstance(author['birth_year'], (int, type(None)))
                if 'death_year' in author:
                    self.assertIsInstance(author['death_year'], (int, type(None)))

    def test_format_structure(self):
        """Test format information structure"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if response.data['results']:
            book = response.data['results'][0]
            if book['formats']:
                format_info = book['formats'][0]
                self.assertIn('mime_type', format_info)
                self.assertIn('url', format_info)
