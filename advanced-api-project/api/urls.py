from django.urls import path
from .views import BookCreateView, BookDeleteView, BookDetailView, BookListView, BookTestUpdateView, BookUpdateView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create', BookCreateView.as_view(), name='book-create'),  # create a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'), #delete a book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'), #Update a book
    path('books/update-test/<int:pk>/', BookTestUpdateView.as_view(), name='book-update-test')
]