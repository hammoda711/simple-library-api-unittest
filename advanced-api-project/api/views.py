from rest_framework import generics
from api.models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import NotFound
# Create your views here.

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailViewView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


    def get_object(self):
        # Get the book ID from the URL
        book_id = self.kwargs.get("pk")
        
        # Custom logic: For example, ensure the book is available (not deleted or flagged)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound("this book does not exist.")
        
        return book

