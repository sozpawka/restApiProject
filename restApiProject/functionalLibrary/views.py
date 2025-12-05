from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Book.objects.all()
        title = self.request.query_params.get("title")
        genre = self.request.query_params.get("genre")
        author = self.request.query_params.get("author")

        if title:
            queryset = queryset.filter(title=title)
        if genre:
            queryset = queryset.filter(genre=genre)
        if author:
            queryset = queryset.filter(author__name=author)

        return queryset
