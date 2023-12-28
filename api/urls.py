from django.urls import path
from django.views.decorators.cache import cache_page

from api.views import AuthorListCreateView, AuthorDetailView, BookListCreateView, BookDetailView

urlpatterns = [
    path('authors/', cache_page(60*60)(AuthorListCreateView.as_view()), name='author-list-create'),
    path('authors/<int:pk>/', cache_page(60*60)(AuthorDetailView.as_view()), name='author-detail'),
    path('books/', cache_page(60*60)(BookListCreateView.as_view()), name='book-list-create'),
    path('books/<int:pk>/', cache_page(60*60)(BookDetailView.as_view()), name='book-detail'),
]
