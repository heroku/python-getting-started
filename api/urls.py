from django.urls import path
from .views import get_books, get_book, add_book, update_book, delete_book, get_authors, get_author

urlpatterns = [
    path('books/', get_books),
    path('books/<int:id>/', get_book),
    path('books/', add_book),
    path('books/<int:id>/', update_book),
    path('books/<int:id>/', delete_book),
    path('authors/', get_authors),
    path('authors/<int:id>/', get_author),
]
