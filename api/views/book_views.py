from rest_framework import generics
from api.models.book_test import Book
from api.serializers import BookSerializer
class ListBooksAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer