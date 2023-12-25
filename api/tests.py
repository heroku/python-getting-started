import json
from django.test import TestCase
from django.urls import reverse
from .models import Book, Author


# Create your tests here.
class BookstoreAPITests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='John Doe')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            genre='Fiction',
            publication_date='2022-01-01'
        )

    def test_get_books(self):
        response = self.client.get(reverse('get_books'))
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        response = self.client.get(reverse('get_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_add_book(self):
        data = {
            'title': 'New Book',
            'author': 'Jane Doe',
            'genre': 'Non-fiction',
            'publication_date': '2023-01-01'
        }
        response = self.client.post(reverse('add_book'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.filter(title='New Book').exists(), True)

    def test_update_book(self):
        data = {'title': 'Updated Book'}
        response = self.client.put(reverse('update_book', args=[self.book.id]), json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        response = self.client.delete(reverse('delete_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.filter(id=self.book.id).exists(), False)

    def test_get_authors(self):
        response = self.client.get(reverse('get_authors'))
        self.assertEqual(response.status_code, 200)

    def test_get_author(self):
        response = self.client.get(reverse('get_author', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
