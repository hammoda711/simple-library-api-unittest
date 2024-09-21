from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['title','author', 'publication_year']
    search_fields = ['title','author__name']
    ordering_fields = '__all__'
    ordering = ['title', 'publication_year'] #default ordering 

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        # Get the book ID from the URL
        book_id = self.kwargs.get("pk")
        
        # Custom logic: For example, ensure the book is available (not deleted or flagged)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound("this book does not exist.")
        
        return book


class BookCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


