from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
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
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def search(self, request):
        title = request.query_params.get('title')
        genre = request.query_params.get('genre')
        author_name = request.query_params.get('author_name')

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title=title)
        if genre:
            queryset = queryset.filter(genre=genre)
        if author_name:
            queryset = queryset.filter(author__name=author_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
