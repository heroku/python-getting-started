from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Book, Author
import json


# Create your views here.
def get_books(request):
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')

    books = Book.objects.all()

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__name__icontains=author)
    if genre:
        books = books.filter(genre__icontains=genre)

    data = [{'id': book.id, 'title': book.title, 'author': book.author.name, 'genre': book.genre,
             'publication_date': book.publication_date} for book in books]

    return JsonResponse(data, safe=False)


def get_book(request, id):
    book = get_object_or_404(Book, id=id)
    data = {'id': book.id, 'title': book.title, 'author': book.author.name, 'genre': book.genre,
            'publication_date': book.publication_date}
    return JsonResponse(data)


def add_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        author = Author.objects.get_or_create(name=data['author'])[0]
        book = Book.objects.create(title=data['title'], author=author, genre=data['genre'],
                                   publication_date=data['publication_date'])
        return JsonResponse({'id': book.id, 'title': book.title, 'author': author.name,
                             'genre': book.genre, 'publication_date': book.publication_date})


def update_book(request, id):
    if request.method == 'PUT':
        book = get_object_or_404(Book, id=id)
        data = json.loads(request.body)

        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            author = Author.objects.get_or_create(name=data['author'])[0]
            book.author = author
        if 'genre' in data:
            book.genre = data['genre']
        if 'publication_date' in data:
            book.publication_date = data['publication_date']

        book.save()

        return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author.name,
                             'genre': book.genre, 'publication_date': book.publication_date})


def delete_book(request, id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=id)
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully'})


def get_authors(request):
    name = request.GET.get('name', '')
    authors = Author.objects.all()

    if name:
        authors = authors.filter(name__icontains=name)

    data = [{'id': author.id, 'name': author.name} for author in authors]
    return JsonResponse(data, safe=False)


def get_author(request, id):
    author = get_object_or_404(Author, id=id)
    data = {'id': author.id, 'name': author.name}
    return JsonResponse(data)
